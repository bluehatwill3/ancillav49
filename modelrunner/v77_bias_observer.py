#!/usr/bin/env python3
"""
HOLOSYN V77: MASTER ALGORITHMIC BIAS & OBJECTIVITY NEXUS
===================================================================================
Hardware Target: Dell Latitude 5420 (i5-1145G7 | 16GB RAM | CPU-Only)
Role: Models Confirmation Bias, SNN Distribution Skewness, and Weight-Level Bias.
Integration: Inspects native PyTorch `.bias` tensors and deploys HF Symbolic Logic.
"""

import sys
import os
import gc
import torch
import torch.nn as nn
import numpy as np
import warnings
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
            print(f"   🧬 [BIAS CORE] Structural objectivity weights mapped from: {os.path.basename(path)}")
            return True
        except Exception: return False


# ──────────────────────────────────────────────────────────────────────
# ⚖️ NATIVE TENSOR BIAS SCANNER (hive_fused_all.pt)
# ──────────────────────────────────────────────────────────────────────
class NativeBiasWeightScanner:
    """
    Directly accesses the local state dictionaries to calculate the physical
    magnitude of `.bias` parameters inside the neural network layers.
    If the biases are massively inflated relative to the weights, the system
    is intrinsically predisposed to a single outcome (Zero-Shot Shift).
    """
    def __init__(self):
        self.device = "cpu"
        self.native_bias_magnitude = 0.5
        self._scan_network_biases()

    def _scan_network_biases(self):
        target_dir = "/home/devcbloom/Documents/Intellibloomenv/lang"
        paths = [
            "hive_fused_all.pt", os.path.join(target_dir, "hive_fused_all.pt"),
            "hive_best.pt", os.path.join(target_dir, "hive_best.pt")
        ]
        
        for p in paths:
            if os.path.exists(p):
                try:
                    weights = torch.load(p, map_location=self.device, weights_only=False)
                    state_dict = weights.state_dict() if hasattr(weights, 'state_dict') else weights
                    
                    bias_tensors = []
                    for key, tensor in state_dict.items():
                        if 'bias' in key and isinstance(tensor, torch.Tensor):
                            bias_tensors.append(tensor.float().abs().mean().item())
                            
                    if bias_tensors:
                        # Normalize the average bias magnitude (Assume > 2.0 is heavily biased)
                        avg_bias = np.mean(bias_tensors)
                        self.native_bias_magnitude = float(np.clip(avg_bias / 2.0, 0.0, 1.0))
                        print(f"   ⚡ [NATIVE BIAS SCANNER] Found {len(bias_tensors)} bias tensors. Magnitude: {self.native_bias_magnitude:.4f}")
                    break
                except Exception: pass

    def get_intrinsic_bias(self):
        # Return how "biased" the network inherently is based on its saved weights
        return self.native_bias_magnitude


# ──────────────────────────────────────────────────────────────────────
# 🧠 HUGGINGFACE SYMBOLIC OBJECTIVITY SWARM
# ──────────────────────────────────────────────────────────────────────
try:
    from transformers import AutoModelForCausalLM, AutoTokenizer
    HF_AVAILABLE = True
except ImportError:
    HF_AVAILABLE = False

class BiasSymbolicMicroSwarm:
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
            print(f"   ⏳ [OBJECTIVITY MICROMODEL] Allocating {model_id} to CPU...")
            self.model = AutoModelForCausalLM.from_pretrained(model_id, torch_dtype=self.dtype).eval()
            self.tokenizer = AutoTokenizer.from_pretrained(model_id)
            self.active = True
            print("   ✅ [OBJECTIVITY MICROMODEL] Symbolic Fairness Engine Locked.")
        except Exception as e: 
            print(f"   ⚠️ [OBJECTIVITY MICROMODEL] Model bypass active. {e}")

    def evaluate_symbolic_objectivity(self, confirmation_bias, snn_skewness):
        if not self.active:
            # Fallback heuristic: Objectivity is the inverse of combined biases
            return float(np.clip(1.0 - (confirmation_bias * 0.5 + abs(snn_skewness) * 0.5), 0.0, 1.0))
            
        prompt = f"System cognitive confirmation bias = {confirmation_bias:.3f}. Neural activation skewness = {snn_skewness:.3f}. Is the framework operating objectively and fairly without hallucinating its own priors? Output only a float between 0.0 (Heavily Biased) and 1.0 (Objective/Unbiased)."
        try:
            inputs = self.tokenizer(prompt, return_tensors="pt")
            with torch.no_grad():
                outputs = self.model.generate(**inputs, max_new_tokens=10, do_sample=False)
            response = self.tokenizer.decode(outputs[0][inputs.input_ids.size(1):], skip_special_tokens=True)
            match = re.search(r"0\.\d+|1\.0", response)
            if match: return float(match.group())
            return float(np.clip(1.0 - confirmation_bias, 0.0, 1.0))
        except Exception: 
            return 0.5


# ──────────────────────────────────────────────────────────────────────
# 📉 NUMERICAL COGNITIVE BIAS ENGINE
# ──────────────────────────────────────────────────────────────────────
class NumericalBiasObserver(BaseObserver):
    """
    Computes real-time execution bias: Confirmation Bias and Distribution Skewness.
    """
    def __init__(self, hive_core=None):
        super().__init__()
        self.hive_core = hive_core if hive_core is not None else HiveFusionCore().eval()

    def calculate_confirmation_bias(self, s, haptic_level):
        """
        Confirmation Bias occurs when the system believes it is highly synchronized (s),
        despite the physical hardware/haptics experiencing severe noise or friction.
        It implies the network is ignoring reality to confirm its own prior state.
        """
        expected_s = 1.0 - haptic_level
        # If actual s is much higher than expected s, we have confirmation bias
        delusion_gap = max(0.0, s - expected_s)
        
        # Normalize into a bias index (0 = objective, 1 = completely delusional)
        confirmation_bias = np.clip(delusion_gap * 1.5, 0.0, 1.0)
        return float(confirmation_bias)

    def calculate_snn_skewness(self, snn):
        """
        Calculates Pearson's median skewness of the neural activation array.
        A highly skewed array implies Attention Bias (focusing heavily on one feature).
        """
        snn_arr = np.array(snn) if (snn is not None and hasattr(snn, '__len__') and len(snn) > 1) else np.array([0.5, 0.5])
        
        mean_val = np.mean(snn_arr)
        median_val = np.median(snn_arr)
        std_val = np.std(snn_arr)
        
        if std_val < 1e-5:
            return 0.0 # Perfectly uniform, no skew
            
        # Pearson's second skewness coefficient
        skewness = 3.0 * (mean_val - median_val) / std_val
        
        # Normalize to [0, 1] magnitude
        normalized_skew_magnitude = np.clip(abs(skewness) / 3.0, 0.0, 1.0)
        return float(normalized_skew_magnitude)


# ──────────────────────────────────────────────────────────────────────
# 🌐 MASTER BIAS & OBJECTIVITY NEXUS ORCHESTRATOR
# ──────────────────────────────────────────────────────────────────────
class UnifiedBiasNexus(BaseObserver):
    def __init__(self):
        super().__init__()
        print("💠 [BIAS NEXUS] Initializing Algorithmic Objectivity & Tensor Diagnostics...")
        
        self.hive_core = HiveFusionCore().eval()
        self._bind_master_weights()
        
        self.native_bias_scanner = NativeBiasWeightScanner()
        self.numerical_engine = NumericalBiasObserver(self.hive_core)
        self.symbolic_engine = BiasSymbolicMicroSwarm()

    def _bind_master_weights(self):
        locations = ["hive_fused_all.pt", "hive_best.pt", "/home/devcbloom/Downloads/hive_fused_all.pt"]
        for path in locations:
            if self.hive_core.assimilate_hive(path):
                break

    def evaluate(self, s, sy, p, snn, text="", haptic_level=0.0, **kwargs):
        
        # 1. Evaluate Execution Delusion (Confirmation Bias)
        confirmation_bias = self.numerical_engine.calculate_confirmation_bias(s, haptic_level)
        
        # 2. Evaluate Attention / Feature Bias (Skewness)
        snn_skewness = self.numerical_engine.calculate_snn_skewness(snn)
        
        # 3. Retrieve Hardware Tensor Bias (Zero-Shot shift of physical model weights)
        intrinsic_weight_bias = self.native_bias_scanner.get_intrinsic_bias()
        
        # 4. Evaluate Symbolic Objectivity using HuggingFace Micro-Model
        symbolic_objectivity = self.symbolic_engine.evaluate_symbolic_objectivity(confirmation_bias, snn_skewness)
        
        # 5. Compute the Master Correction Factor
        # This factor is sent to kwargs so the primary Holosyn governor can actively down-regulate biased states.
        # Objectivity = 1.0 means no correction needed. Objectivity < 0.5 triggers active modification.
        overall_objectivity = (symbolic_objectivity * 0.5) + ((1.0 - intrinsic_weight_bias) * 0.3) + ((1.0 - confirmation_bias) * 0.2)
        bias_correction_factor = np.clip(overall_objectivity, 0.1, 1.0)
        
        # Record into framework pipeline
        kwargs['bias_confirmation'] = confirmation_bias
        kwargs['bias_snn_skewness'] = snn_skewness
        kwargs['bias_intrinsic_weight'] = intrinsic_weight_bias
        kwargs['bias_correction_factor'] = bias_correction_factor  # CRITICAL MODIFIER
        
        print(f"   ⚖️ [COGNITIVE BIAS] Confirmation Bias: {confirmation_bias:.3f} | SNN Skewness: {snn_skewness:.3f}")
        print(f"   ⚡ [PHYSICAL WEIGHT BIAS]: {intrinsic_weight_bias:.4f} | 🤖 [SYMBOLIC OBJECTIVITY]: {symbolic_objectivity:.4f}")

        try:
            snn_density = float(np.mean(snn)) if (snn is not None and hasattr(snn, '__len__') and len(snn) > 0) else 0.5
            
            # Vector allocation: [Coherence, Objectivity, Skewness (Inverse), SNN Density, Symbolic Yield]
            state_matrix = torch.tensor([[[s, bias_correction_factor, (1.0 - snn_skewness), snn_density, symbolic_objectivity]]], dtype=torch.float32)
            
            with torch.no_grad():
                master_judgment = self.hive_core(state_matrix).item()
        except Exception:
            master_judgment = 0.5

        # Compile final unified Objectivity resonance
        final_resonance = np.clip((bias_correction_factor * 0.4) + (master_judgment * 0.6), 0.0, 1.0)
        
        # PENALTY APPLICATION: If the system is highly biased, artificially suppress the resonance
        final_resonance = final_resonance * bias_correction_factor
        
        print(f"📊 [BIAS NEXUS TOTAL RESONANCE (Corrected)]: {final_resonance:.4f}")
        print("═" * 80)
        return float(final_resonance)


# Register global variables for strict validation scanner checks
observer = UnifiedBiasNexus()
plugin_observer = observer

if __name__ == "__main__":
    # Baseline framework execution verification
    observer.evaluate(0.95, 0.90, 0.50, [0.1, 0.9, 0.1, 0.9], text="Evaluating biased system states.", haptic_level=0.8)