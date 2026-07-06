#!/usr/bin/env python3
"""
HOLOSYN V81: MASTER DIMENSIONALITY & MANIFOLD TOPOLOGY NEXUS (ARRAY-SAFE)
===================================================================================
Hardware Target: Dell Latitude 5420 (i5-1145G7 | 16GB RAM | CPU-Only)
Role: Models Spectral Entropy, Effective Rank, and Latent Sparsity Dimension.
Integration: Deploys native student_distilled_export matrices & HF Symbolic Logic.
"""

import sys
import os
import gc
import torch
import torch.nn as nn
import numpy as np
import warnings
import collections
import re

warnings.filterwarnings("ignore")
os.environ["TOKENIZERS_PARALLELISM"] = "false"

# ──────────────────────────────────────────────────────────────────────
# 🔌 INTER-MODULE NAMESPACE BRIDGE
# ──────────────────────────────────────────────────────────────────────
BaseObserver = None
avenues = ['__main__', 'nexus', 'core', 'observer', 'main', 'harvest_manager']
for module_name in avenues:
    if module_name in sys.modules:
        mod = sys.modules[module_name]
        if hasattr(mod, 'BaseObserver'):
            BaseObserver = getattr(mod, 'BaseObserver')
            break

if BaseObserver is None:
    class BaseObserver:
        def evaluate(self, s, sy, p, snn, text="", haptic_level=0.0, **kwargs): 
            return 0.5

# ──────────────────────────────────────────────────────────────────────
# 🧬 HIVE FUSION CENTRAL INTEGRATOR
# ──────────────────────────────────────────────────────────────────────
class HiveFusionCore(nn.Module):
    def __init__(self, in_dim=5, h_dim=32, n_heads=2, n_layers=1):
        super().__init__()
        self.embedding = nn.Linear(in_dim, h_dim)
        self.pos_encoder = nn.Parameter(torch.zeros(1, 512, h_dim))
        encoder_layer = nn.TransformerEncoderLayer(
            d_model=h_dim, nhead=n_heads, dim_feedforward=h_dim * 2, batch_first=True
        )
        self.transformer = nn.TransformerEncoder(encoder_layer, num_layers=n_layers)
        self.projector = nn.Linear(h_dim, 1)

    def forward(self, x):
        if x.dim() < 2 or x.size(1) == 0: 
            return torch.tensor([0.5])
        seq_len = min(x.size(1), 512)
        emb = self.embedding(x[:, :seq_len, :]) + self.pos_encoder[:, :seq_len, :]
        return torch.tanh(self.projector(self.transformer(emb).mean(dim=1)).squeeze(-1))

    def assimilate_hive(self, path):
        if not os.path.exists(path): return False
        try:
            weights = torch.load(path, map_location="cpu", weights_only=False)
            if hasattr(weights, 'state_dict'): weights = weights.state_dict()
            clean_dict = {re.sub(r'^(enc\.|text\.|net\.|0\.|module\.)', '', k): v 
                          for k, v in weights.items() if isinstance(v, torch.Tensor)}
            self.load_state_dict(clean_dict, strict=False)
            print(f"   🧬 [DIMENSIONALITY CORE] Unified manifold mapping from: {os.path.basename(path)}")
            return True
        except Exception: return False


# ──────────────────────────────────────────────────────────────────────
# 🧮 NATIVE LATENT SPARSITY ENCODER (TorchScript)
# ──────────────────────────────────────────────────────────────────────
class NativeDimensionalityEncoder:
    """
    Ingests student_distilled_export.torchscript.pt to measure the "Latent Dimensionality".
    Calculates sparsity (L0 proxy) to see how many internal tensor dimensions are
    actively being used by the model vs remaining dormant.
    """
    def __init__(self):
        self.device = "cpu"
        self.model = None
        self._boot_distilled_tensor()

    def _boot_distilled_tensor(self):
        target_dir = "/home/devcbloom/Documents/Intellibloomenv/lang"
        paths = ["student_distilled_export.torchscript.pt", 
                 os.path.join(target_dir, "student_distilled_export.torchscript.pt")]
        
        for p in paths:
            if os.path.exists(p):
                try:
                    self.model = torch.jit.load(p, map_location=self.device)
                    self.model.eval()
                    print(f"   ⚡ [LATENT ENCODER] Bound localized dimensional matrix: {os.path.basename(p)}")
                    break
                except Exception: pass

    def extract_latent_dimensionality(self, text, snn_array):
        snn_safe = np.array(snn_array) if (snn_array is not None and hasattr(snn_array, '__len__') and len(snn_array) > 0) else np.array([0.5, 0.5])
        
        if not self.model:
            return float(np.mean(snn_safe))
            
        try:
            tokens = [ord(c) % 1000 for c in str(text)[:64]] if text else [1, 0, 1]
            while len(tokens) < 8: tokens.append(0)
            tensor_input = torch.tensor([tokens], dtype=torch.long)
            
            with torch.no_grad():
                out = self.model(tensor_input)
                
            if isinstance(out, tuple): out = out[0]
            
            # Dimensional Sparsity (L0 Norm Proxy): Percentage of output dimensions that are "active"
            # We consider an activation "active" if its absolute value is > 10% of the max activation
            out_flat = out.float().flatten().abs()
            max_act = torch.max(out_flat).item() + 1e-9
            active_dims = torch.sum(out_flat > (0.1 * max_act)).item()
            total_dims = out_flat.numel()
            
            latent_dimension_usage = active_dims / total_dims
            return float(np.clip(latent_dimension_usage, 0.0, 1.0))
        except Exception:
            return float(np.mean(snn_safe))


# ──────────────────────────────────────────────────────────────────────
# 📐 MATHEMATICAL EFFECTIVE DIMENSIONALITY ENGINE
# ──────────────────────────────────────────────────────────────────────
class EffectiveDimensionalityObserver(BaseObserver):
    """
    Computes the Spectral Entropy / Effective Rank of the cognitive state over time.
    """
    def __init__(self, hive_core=None):
        super().__init__()
        self.hive_core = hive_core if hive_core is not None else HiveFusionCore().eval()
        # Rolling buffer to map a 2D surface of recent states
        self.state_history = collections.deque(maxlen=10)

    def calculate_spectral_entropy(self, snn):
        """
        Calculates the Shannon Entropy of the Singular Values of the SNN history.
        This measures the 'Effective Dimensionality' of the execution manifold.
        """
        snn_arr = np.array(snn) if (snn is not None and hasattr(snn, '__len__') and len(snn) > 0) else np.array([0.5, 0.5])
        
        # Standardize size for the history buffer
        if len(snn_arr) > 16: snn_arr = snn_arr[:16]
        elif len(snn_arr) < 16: snn_arr = np.pad(snn_arr, (0, 16 - len(snn_arr)), 'constant')
            
        self.state_history.append(snn_arr)
        
        if len(self.state_history) < 3:
            return 0.5 # Not enough history for manifold calculation
            
        # Create state matrix (Rows = Time, Cols = Features)
        M = np.vstack(self.state_history)
        
        try:
            # SVD Decomposition
            U, S, Vt = np.linalg.svd(M, full_matrices=False)
            
            # Normalize singular values to form a probability distribution
            S_sum = np.sum(S) + 1e-9
            p = S / S_sum
            p = p[p > 0]
            
            # Shannon Entropy of the Spectrum
            spectral_entropy = -np.sum(p * np.log2(p + 1e-9))
            
            # Max possible entropy is log2(N) where N is min(time_steps, features)
            max_entropy = np.log2(min(M.shape)) + 1e-9
            
            # Normalized Effective Dimensionality Index [0, 1]
            effective_dimensionality = spectral_entropy / max_entropy
            return float(np.clip(effective_dimensionality, 0.0, 1.0))
            
        except Exception:
            return 0.5


# ──────────────────────────────────────────────────────────────────────
# 🧠 HUGGINGFACE SYMBOLIC DIMENSIONALITY SWARM
# ──────────────────────────────────────────────────────────────────────
try:
    from transformers import AutoModelForCausalLM, AutoTokenizer
    HF_AVAILABLE = True
except ImportError:
    HF_AVAILABLE = False

class DimensionalSymbolicMicroSwarm:
    def __init__(self):
        self.device = "cpu"
        self.dtype = torch.bfloat16
        self.model = None
        self.tokenizer = None
        self.active = False
        self._boot_model()

    def _boot_model(self):
        if not HF_AVAILABLE: return
        model_id = "Qwen/Qwen2.5-0.5B-Instruct"
        try:
            print(f"   ⏳ [DIMENSIONAL MICROMODEL] Allocating {model_id} to CPU...")
            self.model = AutoModelForCausalLM.from_pretrained(model_id, torch_dtype=self.dtype).eval()
            self.tokenizer = AutoTokenizer.from_pretrained(model_id)
            self.active = True
            print("   ✅ [DIMENSIONAL MICROMODEL] Symbolic Topology Engine Locked.")
        except Exception as e: 
            print(f"   ⚠️ [DIMENSIONAL MICROMODEL] Model bypass active. {e}")

    def evaluate_manifold_complexity(self, effective_dim, latent_dim):
        if not self.active:
            # Fallback heuristic: Balanced dimensionality (around 0.5 to 0.7) is optimal
            # Too low = rigid, too high = pure noise.
            complexity = (effective_dim + latent_dim) / 2.0
            return float(np.clip(1.0 - abs(complexity - 0.6), 0.0, 1.0))
            
        prompt = f"Manifold Effective Dimensionality = {effective_dim:.3f}. Latent Space Sparse Dimension = {latent_dim:.3f}. Is the topological manifold maintaining structural complexity without collapsing into rigid 1D behavior or expanding into pure noise? Output only a float between 0.0 (Collapsed/Noise) and 1.0 (Optimal Manifold)."
        try:
            inputs = self.tokenizer(prompt, return_tensors="pt")
            with torch.no_grad():
                outputs = self.model.generate(**inputs, max_new_tokens=10, do_sample=False)
            response = self.tokenizer.decode(outputs[0][inputs.input_ids.size(1):], skip_special_tokens=True)
            match = re.search(r"0\.\d+|1\.0", response)
            if match: return float(match.group())
            return float(np.clip((effective_dim + latent_dim)/2.0, 0.0, 1.0))
        except Exception: 
            return 0.5


# ──────────────────────────────────────────────────────────────────────
# 🌐 MASTER DIMENSIONALITY NEXUS ORCHESTRATOR
# ──────────────────────────────────────────────────────────────────────
class UnifiedDimensionalityNexus(BaseObserver):
    def __init__(self):
        super().__init__()
        print("💠 [DIMENSIONALITY NEXUS] Initializing Spectral Entropy & Effective Ranks...")
        
        self.hive_core = HiveFusionCore().eval()
        self._bind_master_weights()
        
        self.latent_encoder = NativeDimensionalityEncoder()
        self.math_engine = EffectiveDimensionalityObserver(self.hive_core)
        self.symbolic_engine = DimensionalSymbolicMicroSwarm()

    def _bind_master_weights(self):
        locations = ["hive_fused_all.pt", "hive_best.pt", "/home/devcbloom/Downloads/hive_fused_all.pt"]
        for path in locations:
            if self.hive_core.assimilate_hive(path):
                break

    def evaluate(self, s, sy, p, snn, text="", haptic_level=0.0, **kwargs):
        
        # 1. Evaluate Mathematical Effective Dimensionality (Spectral Entropy)
        effective_dimensionality = self.math_engine.calculate_spectral_entropy(snn)
        
        # 2. Extract Latent Sparsity Dimension via student_distilled_export
        latent_dimensionality = self.latent_encoder.extract_latent_dimensionality(text, snn)
        
        # 3. Evaluate Symbolic Manifold Health using HuggingFace Micro-Model
        symbolic_manifold_yield = self.symbolic_engine.evaluate_manifold_complexity(effective_dimensionality, latent_dimensionality)
        
        # Record into framework pipeline
        kwargs['dim_effective_rank'] = effective_dimensionality
        kwargs['dim_latent_sparsity'] = latent_dimensionality
        kwargs['dim_symbolic_yield'] = symbolic_manifold_yield
        
        print(f"   📐 [TOPOLOGY] Effective Dimensionality (SVD Entropy): {effective_dimensionality:.3f}")
        print(f"   ⚡ [NATIVE LATENT SPARSITY]: {latent_dimensionality:.3f} | 🤖 [SYMBOLIC MANIFOLD YIELD]: {symbolic_manifold_yield:.4f}")

        try:
            snn_density = float(np.mean(snn)) if (snn is not None and hasattr(snn, '__len__') and len(snn) > 0) else 0.5
            
            # Vector allocation: [Coherence, Effective Dim, Latent Dim, SNN Density, Symbolic Yield]
            state_matrix = torch.tensor([[[s, effective_dimensionality, latent_dimensionality, snn_density, symbolic_manifold_yield]]], dtype=torch.float32)
            
            with torch.no_grad():
                master_judgment = self.hive_core(state_matrix).item()
        except Exception:
            master_judgment = 0.5

        # Compile final unified dimensional resonance
        final_resonance = np.clip((effective_dimensionality * 0.3) + (symbolic_manifold_yield * 0.3) + (master_judgment * 0.4), 0.0, 1.0)
        
        print(f"📊 [DIMENSIONALITY NEXUS TOTAL RESONANCE]: {final_resonance:.4f}")
        print("═" * 80)
        return float(final_resonance)


# Register global variables for strict validation scanner checks
observer = UnifiedDimensionalityNexus()
plugin_observer = observer

if __name__ == "__main__":
    # Baseline framework execution verification
    mock_payload = "Mapping internal manifold dimensions and latent degrees of freedom."
    # Double evaluate to populate the time rolling buffer
    observer.evaluate(0.88, 0.92, 0.40, [0.7, 0.6, 0.8, 0.4], text=mock_payload, haptic_level=0.15)
    observer.evaluate(0.85, 0.90, 0.42, [0.6, 0.5, 0.9, 0.3], text=mock_payload, haptic_level=0.10)