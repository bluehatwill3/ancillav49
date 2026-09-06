"""
=========================================================================================
MINIMAX DISTILLED SPIKE TRANSFORMER WITH QUANTUM ERROR MANIFOLD
=========================================================================================
Architecture:
  1. Lexicon Transformation Layer (Text -> Continuous Embeddings)
  2. Spiking Transformer Core (Attention + LIF Dynamics)
  3. Quantum Error Manifold Archive (Cirq Parameterized Circuit Encoding)
  4. Minimax Adversarial Distillation Training Loop
=========================================================================================
"""

import numpy as np
import torch
import torch.nn as nn
import cirq
from typing import List, Tuple


# =======================================================================================
# 1. LEXICON TRANSFORMATION LAYER
# =======================================================================================

class LexiconTransformation(nn.Module):
    """Maps discrete vocabulary tokens into continuous embedding sequences."""
    def __init__(self, vocab_size: int = 4000, embed_dim: int = 128):
        super().__init__()
        self.vocab_size = vocab_size
        self.embedding = nn.Embedding(vocab_size, embed_dim)
        self.w2i = {"<PAD>": 0, "<UNK>": 1, "STEER_LEFT": 2, "ACCELERATE": 3, "ERROR": 4}
        self.counter = 5

    def text_to_tensor(self, text: str, max_len: int = 16) -> torch.Tensor:
        tokens = []
        for word in text.upper().split():
            if word not in self.w2i and self.counter < self.vocab_size:
                self.w2i[word] = self.counter
                self.counter += 1
            tokens.append(self.w2i.get(word, self.w2i["<UNK>"]))
        
        while len(tokens) < max_len:
            tokens.append(self.w2i["<PAD>"])
            
        token_tensor = torch.tensor(tokens[:max_len], dtype=torch.long)
        return self.embedding(token_tensor)  # Shape: (Seq_Len, Embed_Dim)


# =======================================================================================
# 2. SPIKING TRANSFORMER CORE
# =======================================================================================

class SurrogateHeaviside(torch.autograd.Function):
    """Surrogate gradient function enabling backpropagation through binary spikes."""
    @staticmethod
    def forward(ctx, x: torch.Tensor, alpha: float = 2.0) -> torch.Tensor:
        ctx.save_for_backward(x)
        ctx.alpha = alpha
        return (x > 0.0).float()

    @staticmethod
    def backward(ctx, grad_output: torch.Tensor) -> Tuple[torch.Tensor, None]:
        (x,) = ctx.saved_tensors
        grad_input = grad_output * (ctx.alpha / 2.0) / (1.0 + (torch.abs(x) * ctx.alpha)) ** 2
        return grad_input, None


class LIFNode(nn.Module):
    """Leaky Integrate-and-Fire neural membrane dynamics."""
    def __init__(self, decay: float = 0.8, threshold: float = 1.0):
        super().__init__()
        self.decay = decay
        self.threshold = threshold

    def forward(self, x: torch.Tensor, membrane: torch.Tensor) -> Tuple[torch.Tensor, torch.Tensor]:
        membrane = membrane * self.decay + x
        spike = SurrogateHeaviside.apply(membrane - self.threshold)
        membrane = membrane * (1.0 - spike)  # Hard membrane reset
        return spike, membrane


class SpikeTransformer(nn.Module):
    """Multi-Head Attention core driven by discrete LIF spike dynamics."""
    def __init__(self, embed_dim: int, num_heads: int, num_actions: int):
        super().__init__()
        self.attention = nn.MultiheadAttention(embed_dim, num_heads, batch_first=True)
        self.lif = LIFNode()
        self.fc_out = nn.Linear(embed_dim, num_actions)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        # x shape: (BatchSize, SeqLen, EmbedDim)
        attn_out, _ = self.attention(x, x, x)
        
        batch_size, seq_len, embed_dim = attn_out.shape
        membrane = torch.zeros(batch_size, seq_len, embed_dim, device=x.device)
        
        spikes, _ = self.lif(attn_out, membrane)
        pooled_spikes = spikes.mean(dim=1)  # Temporal rate pooling
        
        return self.fc_out(pooled_spikes)


# =======================================================================================
# 3. QUANTUM ERROR MANIFOLD ARCHIVE (CIRQ)
# =======================================================================================

class QuantumManifoldArchive:
    """
    Encodes and archives model error states as entangled quantum circuits using Cirq.
    Only stores representations when the classical error residual exceeds the threshold.
    """
    def __init__(self, num_qubits: int = 4, error_threshold: float = 0.3):
        self.num_qubits = num_qubits
        self.qubits = cirq.LineQubit.range(num_qubits)
        self.simulator = cirq.Simulator()
        self.error_threshold = error_threshold
        self.archive: List[np.ndarray] = []

    def _encode_to_circuit(self, error_vector: np.ndarray) -> cirq.Circuit:
        """Translates a flattened 1D classical error vector into parameterized quantum rotations."""
        circuit = cirq.Circuit()
        norm_val = np.linalg.norm(error_vector) + 1e-8
        norm_vec = (error_vector / norm_val) * np.pi
        
        num_features = len(norm_vec)
        for i, q in enumerate(self.qubits):
            # Ensure scalar float conversion for Cirq gate compatibility
            angle = float(norm_vec[i % num_features])
            circuit.append(cirq.rx(angle)(q))
            circuit.append(cirq.ry(angle)(q))
            
        # Entangle qubits across the manifold
        for i in range(self.num_qubits - 1):
            circuit.append(cirq.CNOT(self.qubits[i], self.qubits[i + 1]))
            
        return circuit

    def evaluate_and_archive(self, error_tensor: torch.Tensor):
        """Archives quantum state vectors strictly when error residual exceeds threshold."""
        # Flatten tensor to a 1D NumPy array to remove batch dimensions
        error_np = error_tensor.detach().cpu().numpy().flatten()
        magnitude = float(np.mean(np.abs(error_np)))
        
        if magnitude > self.error_threshold:
            circuit = self._encode_to_circuit(error_np)
            result = self.simulator.simulate(circuit)
            state_vector = np.around(result.final_state_vector, 5)
            self.archive.append(state_vector)
            print(f"📌 [MANIFOLD] Archived new error state | Magnitude: {magnitude:.4f} | Archive Size: {len(self.archive)}")

    def get_worst_case_penalty(self) -> float:
        """Calculates minimax regularization penalty based on archived manifold density."""
        if not self.archive:
            return 0.0
        return float(np.log1p(len(self.archive)))


# =======================================================================================
# 4. MINIMAX DISTILLATION WORKFLOW
# =======================================================================================

def run_minimax_distillation(steps: int = 2):
    print("=" * 80)
    print("⚡ INITIALIZING MINIMAX SPIKE TRANSFORMER & QUANTUM MANIFOLD PIPELINE")
    print("=" * 80)
    
    lexicon = LexiconTransformation(vocab_size=1000, embed_dim=128)
    model = SpikeTransformer(embed_dim=128, num_heads=4, num_actions=2)
    manifold = QuantumManifoldArchive(num_qubits=4, error_threshold=0.3)
    
    optimizer = torch.optim.Adam(model.parameters(), lr=0.01)
    loss_fn = nn.MSELoss()

    input_text = "STEER_LEFT ACCELERATE"
    target_action = torch.tensor([[1.0, 0.0]])  # Target actuation vector

    for step in range(1, steps + 1):
        print(f"\n--- 🔄 MINIMAX DISTILLATION STEP {step:02d} ---")
        
        # 1. Lexicon Transformation (Text -> Tensors)
        embeddings = lexicon.text_to_tensor(input_text).unsqueeze(0)  # Shape: (1, 16, 128)
        
        # 2. Spiking Forward Pass
        predictions = model(embeddings)
        
        # 3. Compute Residual Error
        task_loss = loss_fn(predictions, target_action)
        error_residual = predictions - target_action
        
        # 4. Conditional Quantum Manifold Archiving
        manifold.evaluate_and_archive(error_residual)
        
        # 5. Minimax Loss: min_theta [ TaskLoss(theta) + lambda * max_e(ManifoldPenalty) ]
        adversarial_penalty = manifold.get_worst_case_penalty()
        total_loss = task_loss + (0.1 * adversarial_penalty)
        
        # 6. Backward Pass
        optimizer.zero_grad()
        total_loss.backward()
        optimizer.step()
        
        print(f"📊 Task Loss: {task_loss.item():.4f} | Manifold Penalty: {adversarial_penalty:.4f} | Total Loss: {total_loss.item():.4f}")


if __name__ == "__main__":
    run_minimax_distillation(steps=2)