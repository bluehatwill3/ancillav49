"""
=========================================================================================
UNIFIED AUTONOMOUS SUITE: DUAL-PHASE DISTILLATION & KNOWLEDGE REASONING (FIXED)
=========================================================================================
Fixes:
  1. Added 'minimax_lambda' to Config.
  2. Fixed temporal tensor expansion in SpikeTransformerLAM to preserve batch dimensions.
  3. Ensured proper scalar casting for Cirq quantum manifold archiving.
=========================================================================================
"""

import time
import math
import numpy as np
import cirq
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data import Dataset, DataLoader

# =======================================================================================
# 1. SYSTEM CONFIGURATION
# =======================================================================================

class Config:
    vocab_size: int = 1000
    embed_dim: int = 128
    hidden_dim: int = 256
    proof_dim: int = 128
    action_dim: int = 4            
    num_heads: int = 4
    time_steps: int = 12
    lif_decay: float = 0.85
    lif_threshold: float = 1.0
    num_qubits: int = 4
    manifold_error_threshold: float = 0.35
    distillation_alpha: float = 0.5   # Balance between Task Loss and Teacher Mimicry
    minimax_lambda: float = 0.10       # Adversarial penalty weighting
    device: str = "cuda" if torch.cuda.is_available() else "cpu"

CONFIG = Config()

# =======================================================================================
# 2. CORE NEURAL COMPONENTS (SURROGATE, LIF, SNN, MANIFOLD)
# =======================================================================================

class SurrogateHeaviside(torch.autograd.Function):
    @staticmethod
    def forward(ctx, x, alpha=2.0):
        ctx.save_for_backward(x)
        ctx.alpha = alpha
        return (x > 0.0).float()

    @staticmethod
    def backward(ctx, grad_output):
        (x,) = ctx.saved_tensors
        grad = grad_output * (ctx.alpha / 2.0) / (1.0 + (torch.abs(x) * ctx.alpha)) ** 2
        return grad, None


class LIFLayer(nn.Module):
    def __init__(self, in_dim: int, out_dim: int, decay: float = 0.85):
        super().__init__()
        self.synapse = nn.Linear(in_dim, out_dim)
        self.decay = decay

    def forward(self, x_seq: torch.Tensor) -> torch.Tensor:
        # x_seq shape: (TimeSteps, BatchSize, InDim)
        time_steps, batch_size, _ = x_seq.shape
        mem = torch.zeros(batch_size, self.synapse.out_features, device=x_seq.device)
        spikes = []
        
        for t in range(time_steps):
            mem = mem * self.decay + self.synapse(x_seq[t])
            spike = SurrogateHeaviside.apply(mem - CONFIG.lif_threshold)
            mem = mem * (1.0 - spike)
            spikes.append(spike)
            
        return torch.stack(spikes, dim=0)  # (TimeSteps, BatchSize, OutDim)


class SpikeTransformerLAM(nn.Module):
    """Spiking Large Action Model mapping text and reasoning into control potentials."""
    def __init__(self):
        super().__init__()
        self.lexicon = nn.Embedding(CONFIG.vocab_size, CONFIG.embed_dim)
        self.input_fusion = nn.Linear(CONFIG.embed_dim * 2, CONFIG.hidden_dim)
        self.attention = nn.MultiheadAttention(CONFIG.hidden_dim, CONFIG.num_heads, batch_first=True)
        self.snn1 = LIFLayer(CONFIG.hidden_dim, CONFIG.hidden_dim, decay=CONFIG.lif_decay)
        self.action_head = nn.Linear(CONFIG.hidden_dim, CONFIG.action_dim)

    def forward(self, text_tokens: torch.Tensor, reasoning_vec: torch.Tensor) -> Tuple[torch.Tensor, torch.Tensor]:
        # 1. Embed and pool token representations: (BatchSize, EmbedDim)
        lex_embeds = self.lexicon(text_tokens).mean(dim=1) 
        
        # 2. Fuse lexicon and reasoning features: (BatchSize, HiddenDim)
        fused = torch.cat([lex_embeds, reasoning_vec], dim=-1)
        fused_hidden = self.input_fusion(fused).unsqueeze(1)  # (BatchSize, 1, HiddenDim)

        # 3. Attention calculation: (BatchSize, 1, HiddenDim)
        attn_out, _ = self.attention(fused_hidden, fused_hidden, fused_hidden)

        # 4. Correct temporal expansion: (TimeSteps, BatchSize, HiddenDim)
        seq_input = attn_out.squeeze(1).unsqueeze(0).repeat(CONFIG.time_steps, 1, 1)

        # 5. Spiking dynamics & Rate pooling across time
        spikes = self.snn1(seq_input)                         # (TimeSteps, BatchSize, HiddenDim)
        mean_firing = spikes.mean(dim=0)                      # (BatchSize, HiddenDim)
        action_preds = self.action_head(mean_firing)          # (BatchSize, ActionDim)

        return action_preds, spikes


class QuantumManifoldArchive:
    """Cirq-Powered Error Archive for Minimax Penalties."""
    def __init__(self):
        self.qubits = cirq.LineQubit.range(CONFIG.num_qubits)
        self.simulator = cirq.Simulator()
        self.archive: List[np.ndarray] = []

    def evaluate_and_archive(self, error_tensor: torch.Tensor):
        flat_err = error_tensor.detach().cpu().numpy().flatten()
        magnitude = float(np.mean(np.abs(flat_err)))

        if magnitude > CONFIG.manifold_error_threshold:
            circuit = cirq.Circuit()
            norm_val = np.linalg.norm(flat_err) + 1e-8
            norm_vec = (flat_err / norm_val) * np.pi
            num_f = len(norm_vec)
            
            for i, q in enumerate(self.qubits):
                circuit.append(cirq.rx(float(norm_vec[i % num_f]))(q))
            for i in range(CONFIG.num_qubits - 1):
                circuit.append(cirq.CNOT(self.qubits[i], self.qubits[i + 1]))
                
            state_vector = np.around(self.simulator.simulate(circuit).final_state_vector, 5)
            self.archive.append(state_vector)

    def get_minimax_penalty(self) -> float:
        return float(np.log1p(len(self.archive))) if self.archive else 0.0


# =======================================================================================
# 3. DATASETS (SYNTHETIC & ORGANIC)
# =======================================================================================

class SyntheticFarmDataset(Dataset):
    def __init__(self, num_samples: int = 128):
        self.num_samples = num_samples

    def __len__(self):
        return self.num_samples

    def __getitem__(self, idx):
        tokens = torch.randint(2, 500, (16,))
        reasoning = torch.randn(CONFIG.embed_dim) 
        target_action = torch.clamp(torch.randn(CONFIG.action_dim), -1.0, 1.0)
        return tokens, reasoning, target_action


class OrganicFarmDataset(Dataset):
    def __init__(self, synthetic_dataset: SyntheticFarmDataset, noise_level: float = 0.3):
        self.synth = synthetic_dataset
        self.noise_level = noise_level

    def __len__(self):
        return len(self.synth)

    def __getitem__(self, idx):
        tokens, reasoning, target_action = self.synth[idx]
        noise = torch.randn_like(reasoning) * self.noise_level
        organic_reasoning = reasoning + noise
        
        dropout_mask = torch.rand_like(tokens.float()) > 0.15
        organic_tokens = tokens * dropout_mask.long()

        return organic_tokens, organic_reasoning, target_action


# =======================================================================================
# 4. TRAINING & DISTILLATION PIPELINE
# =======================================================================================

def run_dual_phase_training():
    print("=" * 80)
    print("🌾 INITIATING DUAL-PHASE KNOWLEDGE DISTILLATION PIPELINE")
    print("=" * 80)

    # 1. Initialize Datasets & Loaders
    synth_dataset = SyntheticFarmDataset(num_samples=128)
    organic_dataset = OrganicFarmDataset(synth_dataset, noise_level=0.35)
    
    synth_loader = DataLoader(synth_dataset, batch_size=16, shuffle=True)
    organic_loader = DataLoader(organic_dataset, batch_size=16, shuffle=True)

    # 2. Initialize Models & Optimizers
    teacher_model = SpikeTransformerLAM().to(CONFIG.device)
    student_model = SpikeTransformerLAM().to(CONFIG.device)
    manifold = QuantumManifoldArchive()
    
    mse_loss = nn.MSELoss()

    # -----------------------------------------------------------------------
    # PHASE 1: PRE-TRAIN TEACHER ON SYNTHETIC DATA
    # -----------------------------------------------------------------------
    print("\n[PHASE 1] Pre-training Teacher Model on Pure Synthetic Telemetry...")
    teacher_optimizer = torch.optim.AdamW(teacher_model.parameters(), lr=2e-3)
    teacher_model.train()
    
    for epoch in range(2):
        for tokens, reasoning, targets in synth_loader:
            tokens = tokens.to(CONFIG.device)
            reasoning = reasoning.to(CONFIG.device)
            targets = targets.to(CONFIG.device)
            
            preds, _ = teacher_model(tokens, reasoning)
            loss = mse_loss(preds, targets)
            
            teacher_optimizer.zero_grad()
            loss.backward()
            teacher_optimizer.step()
        
    print(f"✅ Phase 1 Complete. Teacher Model Synthetically Optimized. (Final Loss: {loss.item():.4f})")
    
    # Freeze Teacher parameters
    teacher_model.eval()
    for param in teacher_model.parameters():
        param.requires_grad = False

    # -----------------------------------------------------------------------
    # PHASE 2: DISTILLATION ON ORGANIC DATA WITH QUANTUM MINIMAX
    # -----------------------------------------------------------------------
    print("\n[PHASE 2] Distilling Student Model on Noisy Organic Telemetry...")
    student_optimizer = torch.optim.AdamW(student_model.parameters(), lr=2e-3)
    student_model.train()

    epochs = 3
    for epoch in range(1, epochs + 1):
        for step, (org_tokens, org_reasoning, targets) in enumerate(organic_loader):
            org_tokens = org_tokens.to(CONFIG.device)
            org_reasoning = org_reasoning.to(CONFIG.device)
            targets = targets.to(CONFIG.device)

            # Teacher forward pass (target anchor)
            with torch.no_grad():
                teacher_action, teacher_spikes = teacher_model(org_tokens, org_reasoning)

            # Student forward pass
            student_action, student_spikes = student_model(org_tokens, org_reasoning)

            # Loss: Task loss + Neural spike mimicry loss
            task_loss = mse_loss(student_action, targets)
            distill_loss = mse_loss(student_spikes.mean(dim=0), teacher_spikes.mean(dim=0))
            
            # Quantum Manifold update
            residual_error = student_action - targets
            manifold.evaluate_and_archive(residual_error)
            adversarial_penalty = manifold.get_minimax_penalty()

            # Minimax weighted objective
            alpha = CONFIG.distillation_alpha
            lam = CONFIG.minimax_lambda
            total_loss = (alpha * task_loss) + ((1.0 - alpha) * distill_loss) + (lam * adversarial_penalty)

            student_optimizer.zero_grad()
            total_loss.backward()
            student_optimizer.step()

        print(f"  Epoch {epoch:02d}/{epochs:02d} | Task Loss: {task_loss.item():.4f} | Distill Loss: {distill_loss.item():.4f} | Q-Penalty: {adversarial_penalty:.4f} | Total: {total_loss.item():.4f}")

    print("\n✅ Phase 2 Complete. Student Model Distilled and Ready for Edge Deployment.")


if __name__ == "__main__":
    run_dual_phase_training()