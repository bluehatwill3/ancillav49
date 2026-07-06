#!/usr/bin/env python3
"""
HOLOSYN V72: MASTER LINEAR ALGEBRA & SYMBOLIC MATRIX NEXUS (ARRAY-SAFE)
===================================================================================
Hardware Target: Dell Latitude 5420 (i5-1145G7 | 16GB RAM | CPU-Only)
Role: Models SVD, Matrix Condition Numbers, and Null Space mapping.
Patch: Fixed NumPy truth value ambiguity in SVD and JIT encoder array checks.
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
            print(f"   🧬 [LINEAR ALG CORE] Unified master weights from: {os.path.basename(path)}")
            return True
        except Exception: return False


# ──────────────────────────────────────────────────────────────────────
# 🧠 DISTILLED STUDENT HEADS (TorchScript Matrix Encoders)
# ──────────────────────────────────────────────────────────────────────
class TorchScriptMatrixEncoder:
    """
    Ingests the local student_distilled_*.torchscript.pt files to extract
    specialized linear algebra latent projections on the CPU.
    """
    def __init__(self):
        self.device = "cpu"
        self.models = {}
        self._boot_distilled_heads()

    def _boot_distilled_heads(self):
        target_dir = "/home/devcbloom/Documents/Intellibloomenv/lang"
        candidate_files = [
            "student_distilled_export.torchscript.pt",
            "student_distilled_heads.torchscript.pt",
            "student_distilled_heads_hf.torchscript.pt",
            "student_distilled_heads_hf.torchscript (1).pt"
        ]
        
        for file in candidate_files:
            paths = [file, os.path.join(target_dir, file)]
            for p in paths:
                if os.path.exists(p):
                    try:
                        model = torch.jit.load(p, map_location=self.device)
                        model.eval()
                        self.models[file] = model
                        print(f"   ⚡ [JIT MATRIX ENCODER] Bound distilled native core: {file}")
                        break
                    except Exception: pass

    def extract_matrix_projection(self, text, snn_array):
        # 🛠️ FIXED: Array-safe check on snn_array
        if not self.models: 
            return float(np.mean(snn_array)) if (snn_array is not None and hasattr(snn_array, '__len__') and len(snn_array) > 0) else 0.5
        
        try:
            tokens = [ord(c) % 1000 for c in str(text)[:64]] if text else [1, 0, 1]
            while len(tokens) < 8: tokens.append(0)
            tensor_input = torch.tensor([tokens], dtype=torch.long)
            
            core_name = list(self.models.keys())[0]
            with torch.no_grad():
                out = self.models[core_name](tensor_input)
                
            if isinstance(out, tuple): out = out[0]
            l2_norm = torch.linalg.vector_norm(out.float()).item()
            return float(np.clip(l2_norm / 100.0, 0.0, 1.0))
        except Exception:
            return 0.5


# ──────────────────────────────────────────────────────────────────────
# 🗣️ HUGGINGFACE TINYLLAMA & MATH SYMBOLIC SWARM
# ──────────────────────────────────────────────────────────────────────
try:
    from transformers import AutoTokenizer, AutoModelForCausalLM
    HF_AVAILABLE = True
except ImportError:
    HF_AVAILABLE = False

class HuggingFaceLinearSwarm:
    def __init__(self):
        self.dtype = torch.bfloat16
        self.llama_active = False
        self.math_active = False
        self._boot_models()

    def _boot_models(self):
        if not HF_AVAILABLE: return
        
        try:
            print("   ⏳ [TINYLLAMA 1.1B] Allocating symbolic logic mesh to CPU...")
            self.llama_tok = AutoTokenizer.from_pretrained("TinyLlama/TinyLlama-1.1B-Chat-v1.0")
            self.llama_mod = AutoModelForCausalLM.from_pretrained("TinyLlama/TinyLlama-1.1B-Chat-v1.0", torch_dtype=self.dtype).eval()
            self.llama_active = True
            print("   ✅ [TINYLLAMA 1.1B] Linguistic/Logic Mesh Locked.")
        except Exception as e: print(f"   ⚠️ Llama Boot Fault: {e}")

        try:
            print("   ⏳ [MATH 0.5B] Allocating algebraic micro-model...")
            self.math_tok = AutoTokenizer.from_pretrained("Qwen/Qwen2.5-0.5B-Instruct")
            self.math_mod = AutoModelForCausalLM.from_pretrained("Qwen/Qwen2.5-0.5B-Instruct", torch_dtype=self.dtype).eval()
            self.math_active = True
            print("   ✅ [MATH 0.5B] Matrix Evaluation Mesh Locked.")
        except Exception as e: print(f"   ⚠️ Math Boot Fault: {e}")

    def evaluate_matrix_symbolism(self, rank, condition_number):
        if not self.math_active:
            return float(np.clip(1.0 - (condition_number / 100.0), 0.0, 1.0))
            
        prompt = f"Matrix Rank = {rank}. Condition Number k(A) = {condition_number:.2f}. Is the matrix singular or ill-conditioned? Output a float between 0.0 (Singular/Chaotic) and 1.0 (Full Rank/Stable)."
        try:
            inputs = self.math_tok(prompt, return_tensors="pt")
            with torch.no_grad():
                out = self.math_mod.generate(**inputs, max_new_tokens=10)
            res = self.math_tok.decode(out[0][inputs.input_ids.size(1):], skip_special_tokens=True)
            match = re.search(r"0\.\d+|1\.0", res)
            if match: return float(match.group())
            return float(np.clip(1.0 - (condition_number / 50.0), 0.0, 1.0))
        except Exception: return 0.5


# ──────────────────────────────────────────────────────────────────────
# 🧮 WOLFRAM-STYLE SYMBOLIC LINEAR ALGEBRA CORE
# ──────────────────────────────────────────────────────────────────────
class WolframSymbolicLinearObserver(BaseObserver):
    """
    Simulates Wolfram Alpha step-by-step matrix decompositions.
    Evaluates the SNN state as a dynamic linear transformation block.
    """
    def __init__(self, hive_core=None):
        super().__init__()
        self.hive_core = hive_core if hive_core is not None else HiveFusionCore().eval()

    def evaluate_svd_and_condition(self, snn):
        """
        Computes Singular Value Decomposition (SVD) and Condition Number (Kappa).
        A high condition number means the system is highly sensitive to noise/haptics.
        """
        # 🛠️ FIXED: Replaced 'not snn' with 'snn is None' to strictly avoid NumPy boolean ambiguity
        if snn is None or not hasattr(snn, '__len__') or len(snn) < 4:
            snn_arr = np.array([0.5, 0.6, 0.4, 0.5])
        else:
            snn_arr = np.array(snn[:4]) # Slice to 4 elements to ensure square 2x2 matrix
            
        matrix_A = snn_arr.reshape(2, 2)
        
        try:
            U, singular_values, Vt = np.linalg.svd(matrix_A)
            rank = np.sum(singular_values > 1e-5)
            sigma_max = np.max(singular_values)
            sigma_min = np.min(singular_values)
            condition_number = sigma_max / (sigma_min + 1e-9)
            stability_metric = np.clip(1.0 / (1.0 + np.log10(condition_number + 1.0)), 0.0, 1.0)
            
            return int(rank), float(condition_number), float(stability_metric)
        except Exception:
            return 2, 1.0, 0.5


# ──────────────────────────────────────────────────────────────────────
# 🌐 MASTER LINEAR ALGEBRA NEXUS ORCHESTRATOR
# ──────────────────────────────────────────────────────────────────────
class UnifiedLinearAlgebraNexus(BaseObserver):
    def __init__(self):
        super().__init__()
        print("💠 [LINEAR ALGEBRA NEXUS] Initializing SVD Matrices & TinyLlama Subsystems...")
        
        self.hive_core = HiveFusionCore().eval()
        self._bind_master_weights()
        
        self.jit_engine = TorchScriptMatrixEncoder()
        self.hf_swarm = HuggingFaceLinearSwarm()
        self.wolfram_engine = WolframSymbolicLinearObserver(self.hive_core)

    def _bind_master_weights(self):
        locations = ["hive_fused_all.pt", "hive_best.pt", "/home/devcbloom/Downloads/hive_fused_all.pt"]
        for path in locations:
            if self.hive_core.assimilate_hive(path):
                break

    def evaluate(self, s, sy, p, snn, text="", haptic_level=0.0, **kwargs):
        # 1. Execute Wolfram-Style SVD Matrix Math
        rank, cond_number, algebraic_stability = self.wolfram_engine.evaluate_svd_and_condition(snn)
        
        # 2. Execute JIT Matrix Encoder Latent Space extraction
        jit_frobenius_norm = self.jit_engine.extract_matrix_projection(text, snn)
        
        # 3. Request Symbolic Reasoning from TinyLlama/Math Swarm
        symbolic_matrix_yield = self.hf_swarm.evaluate_matrix_symbolism(rank, cond_number)
        
        kwargs['lin_matrix_rank'] = rank
        kwargs['lin_condition_kappa'] = cond_number
        kwargs['lin_jit_norm'] = jit_frobenius_norm
        kwargs['lin_symbolic_yield'] = symbolic_matrix_yield
        
        print(f"   🧮 [LINEAR ALGEBRA] Rank: {rank} | Condition κ(A): {cond_number:.2f} | JIT F-Norm: {jit_frobenius_norm:.4f}")
        print(f"   🤖 [HF SWARM SYMBOLIC MATRIX YIELD]: {symbolic_matrix_yield:.4f}")

        try:
            snn_density = np.mean(snn) if (snn is not None and len(snn) > 0) else 0.5
            state_matrix = torch.tensor([[[s, sy, algebraic_stability, jit_frobenius_norm, symbolic_matrix_yield]]], dtype=torch.float32)
            
            with torch.no_grad():
                master_judgment = self.hive_core(state_matrix).item()
        except Exception:
            master_judgment = 0.5

        final_resonance = np.clip((algebraic_stability * 0.3) + (symbolic_matrix_yield * 0.3) + (master_judgment * 0.4), 0.0, 1.0)
        
        print(f"📊 [LINEAR ALGEBRA TOTAL RESONANCE]: {final_resonance:.4f}")
        print("═" * 80)
        return float(final_resonance)


# Register global variables to cleanly clear validation checks
observer = UnifiedLinearAlgebraNexus()
plugin_observer = observer

if __name__ == "__main__":
    mock_text = "Computing orthogonal basis functions for hardware state manifolds."
    observer.evaluate(0.85, 0.90, 0.40, [0.8, 0.2, 0.4, 0.9], text=mock_text, haptic_level=0.1)
