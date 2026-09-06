#!/usr/bin/env python3
"""
HOLOSYN V75: MASTER STATISTICAL & PROBABILISTIC NEXUS (ARRAY-SAFE)
===================================================================================
Hardware Target: Dell Latitude 5420 (i5-1145G7 | 16GB RAM | CPU-Only)
Role: Models Bayesian Inference, Z-Scores, Markov Dynamics, and Variance.
Integration: Deploys Qwen 0.5B and TorchScript models for statistical extraction.
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
            print(f"   🧬 [STATISTICAL CORE] Master weights linked for inference: {os.path.basename(path)}")
            return True
        except Exception: return False


# ──────────────────────────────────────────────────────────────────────
# 🧠 DISTILLED STUDENT HEADS (TorchScript Variance Encoders)
# ──────────────────────────────────────────────────────────────────────
class TorchScriptVarianceEncoder:
    """
    Ingests the local student_distilled_*.torchscript.pt files to extract
    latent standard deviation and variance (statistical noise) from the execution state.
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
            "student_distilled_heads_hf.torchscript.pt"
        ]
        
        for file in candidate_files:
            paths = [file, os.path.join(target_dir, file)]
            for p in paths:
                if os.path.exists(p):
                    try:
                        model = torch.jit.load(p, map_location=self.device)
                        model.eval()
                        self.models[file] = model
                        print(f"   ⚡ [JIT VARIANCE ENCODER] Bound distilled native core: {file}")
                        break
                    except Exception: pass

    def extract_latent_variance(self, text, snn_array):
        # Array-safe existence check
        if not self.models: 
            return float(np.std(snn_array)) if (snn_array is not None and hasattr(snn_array, '__len__') and len(snn_array) > 0) else 0.5
        
        try:
            # Tokenize abstract logic
            tokens = [ord(c) % 1000 for c in str(text)[:64]] if text else [1, 0, 1]
            while len(tokens) < 8: tokens.append(0)
            tensor_input = torch.tensor([tokens], dtype=torch.long)
            
            core_name = list(self.models.keys())[0]
            with torch.no_grad():
                out = self.models[core_name](tensor_input)
                
            if isinstance(out, tuple): out = out[0]
            
            # Calculate standard deviation (variance square root) of the distilled latent tensor
            latent_std = torch.std(out.float()).item()
            
            # High variance = high noise. We return the normalized stability (1.0 - noise)
            return float(np.clip(1.0 - (latent_std / 10.0), 0.0, 1.0))
        except Exception:
            return 0.5


# ──────────────────────────────────────────────────────────────────────
# 🗣️ HUGGINGFACE SYMBOLIC STATISTICAL SWARM
# ──────────────────────────────────────────────────────────────────────
try:
    from transformers import AutoTokenizer, AutoModelForCausalLM
    HF_AVAILABLE = True
except ImportError:
    HF_AVAILABLE = False

class StatisticalSymbolicMicroSwarm:
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
            print(f"   ⏳ [STATISTICAL MICROMODEL] Allocating {model_id} to CPU...")
            self.tokenizer = AutoTokenizer.from_pretrained(model_id)
            self.model = AutoModelForCausalLM.from_pretrained(model_id, torch_dtype=self.dtype).eval()
            self.active = True
            print("   ✅ [STATISTICAL MICROMODEL] Symbolic P-Value Engine Locked.")
        except Exception: pass

    def evaluate_statistical_significance(self, z_score, bayesian_posterior):
        if not self.active:
            return float(np.clip(bayesian_posterior - (abs(z_score) * 0.1), 0.0, 1.0))
            
        prompt = f"Z-Score = {z_score:.2f}. Bayesian Posterior Probability = {bayesian_posterior:.2f}. Is the systemic state statistically significant and stable? Output a float from 0.0 (Unstable/Anomalous) to 1.0 (Stable/Expected)."
        try:
            inputs = self.tokenizer(prompt, return_tensors="pt")
            with torch.no_grad():
                outputs = self.model.generate(**inputs, max_new_tokens=10, do_sample=False)
            res = self.tokenizer.decode(outputs[0][inputs.input_ids.size(1):], skip_special_tokens=True)
            match = re.search(r"0\.\d+|1\.0", res)
            if match: return float(match.group())
            return float(np.clip(bayesian_posterior, 0.0, 1.0))
        except Exception: return 0.5


# ──────────────────────────────────────────────────────────────────────
# 📉 NUMERICAL STATISTICAL ENGINE (BAYES, MARKOV, Z-SCORE)
# ──────────────────────────────────────────────────────────────────────
class NumericalStatisticalObserver(BaseObserver):
    """
    Simulates stochastic math models on system telemetry arrays.
    """
    def __init__(self, hive_core=None):
        super().__init__()
        self.hive_core = hive_core if hive_core is not None else HiveFusionCore().eval()
        
        # Bayesian prior probability of system stability
        self.prior_stability = 0.8
        
        # SNN moving average baseline for Z-score calc
        self.historical_snn_mean = 0.5
        self.historical_snn_std = 0.1

    def calculate_bayesian_posterior(self, s, haptic_level):
        """
        P(Stable | Data) = P(Data | Stable) * P(Stable) / P(Data)
        """
        # P(Stable): Our current prior belief
        prior = self.prior_stability
        
        # P(Data | Stable): The likelihood of observing the current haptic noise IF the system is stable.
        # High noise is very unlikely in a truly stable system.
        likelihood = np.clip(1.0 - haptic_level, 0.01, 0.99)
        
        # P(Data | Unstable): The likelihood of observing this noise if the system is crashing.
        likelihood_unstable = np.clip(haptic_level, 0.01, 0.99)
        
        # Marginal likelihood P(Data) (Law of Total Probability)
        marginal_data = (likelihood * prior) + (likelihood_unstable * (1.0 - prior))
        
        # Bayesian Update
        posterior = (likelihood * prior) / (marginal_data + 1e-9)
        
        # Update the prior for the next execution tick (Markov property)
        self.prior_stability = posterior
        return float(posterior)

    def calculate_z_score(self, snn):
        """
        Calculates how many standard deviations the current state is from the historical mean.
        """
        # Safe array handling
        if snn is None or not hasattr(snn, '__len__') or len(snn) == 0:
            current_mean = 0.5
        else:
            current_mean = float(np.mean(snn))
            
        # Update historical trackers smoothly
        self.historical_snn_mean = (self.historical_snn_mean * 0.9) + (current_mean * 0.1)
        current_std = float(np.std(snn)) if hasattr(snn, '__len__') and len(snn) > 1 else 0.1
        self.historical_snn_std = (self.historical_snn_std * 0.9) + (current_std * 0.1)
        
        # Z-Score formula: Z = (X - mu) / sigma
        z_score = (current_mean - self.historical_snn_mean) / (self.historical_snn_std + 1e-9)
        
        # A high absolute Z-Score means an extreme statistical outlier (anomaly).
        # We normalize this into an anomaly confidence score [0, 1].
        normalized_z_anomaly = np.clip(1.0 - (abs(z_score) / 3.0), 0.0, 1.0)
        return float(z_score), float(normalized_z_anomaly)

    def calculate_markov_transition(self, sy):
        """
        Models the probability of transitioning from a STABLE state to a CHAOTIC state.
        Uses synchronization (sy) as the driving stochastic variable.
        """
        # P(Stable -> Stable)
        p_ss = np.clip(sy, 0.1, 0.99)
        # P(Stable -> Chaotic)
        p_sc = 1.0 - p_ss
        
        return float(p_ss), float(p_sc)


# ──────────────────────────────────────────────────────────────────────
# 🌐 MASTER STATISTICAL NEXUS ORCHESTRATOR
# ──────────────────────────────────────────────────────────────────────
class UnifiedStatisticalNexus(BaseObserver):
    def __init__(self):
        super().__init__()
        print("💠 [STATISTICAL NEXUS] Initializing Bayesian Infrence & Markov Dynamics...")
        
        self.hive_core = HiveFusionCore().eval()
        self._bind_master_weights()
        
        self.jit_engine = TorchScriptVarianceEncoder()
        self.symbolic_engine = StatisticalSymbolicMicroSwarm()
        self.numerical_engine = NumericalStatisticalObserver(self.hive_core)

    def _bind_master_weights(self):
        locations = ["hive_fused_all.pt", "hive_best.pt", "/home/devcbloom/Downloads/hive_fused_all.pt"]
        for path in locations:
            if self.hive_core.assimilate_hive(path):
                break

    def evaluate(self, s, sy, p, snn, text="", haptic_level=0.0, **kwargs):
        # 1. Evaluate Bayesian Posterior (Belief Update)
        bayesian_posterior = self.numerical_engine.calculate_bayesian_posterior(s, haptic_level)
        
        # 2. Evaluate Z-Score and Anomaly Deviation
        z_score, norm_z_anomaly = self.numerical_engine.calculate_z_score(snn)
        
        # 3. Evaluate Markov Chain Transition State
        p_stable_stable, p_stable_chaos = self.numerical_engine.calculate_markov_transition(sy)
        
        # 4. Extract Latent Variance from Student TorchScript models
        latent_variance_stability = self.jit_engine.extract_latent_variance(text, snn)
        
        # 5. Execute Symbolic HuggingFace Math
        symbolic_stat_yield = self.symbolic_engine.evaluate_statistical_significance(z_score, bayesian_posterior)
        
        # Record variables for global scope access
        kwargs['stat_bayesian_post'] = bayesian_posterior
        kwargs['stat_z_score'] = z_score
        kwargs['stat_markov_p_sc'] = p_stable_chaos
        kwargs['stat_latent_stability'] = latent_variance_stability
        
        print(f"   📉 [STATISTICS] Bayes Posterior: {bayesian_posterior:.3f} | Z-Score: {z_score:+.2f} | P(S->Chaos): {p_stable_chaos*100:.1f}%")
        print(f"   🤖 [SYMBOLIC STATISTICAL YIELD]: {symbolic_stat_yield:.4f} | JIT Stability: {latent_variance_stability:.4f}")

        try:
            snn_density = float(np.mean(snn)) if (snn is not None and hasattr(snn, '__len__') and len(snn) > 0) else 0.5
            
            # Vector allocation mapping: [Sync, Bayes Prob, Z-Anomaly, SNN Density, Symbolic Yield]
            state_matrix = torch.tensor([[[s, bayesian_posterior, norm_z_anomaly, snn_density, symbolic_stat_yield]]], dtype=torch.float32)
            
            with torch.no_grad():
                master_judgment = self.hive_core(state_matrix).item()
        except Exception:
            master_judgment = 0.5

        # Compile final unified statistical resonance
        final_resonance = np.clip((bayesian_posterior * 0.3) + (symbolic_stat_yield * 0.3) + (master_judgment * 0.4), 0.0, 1.0)
        
        print(f"📊 [STATISTICAL NEXUS TOTAL RESONANCE]: {final_resonance:.4f}")
        print("═" * 80)
        return float(final_resonance)


# Register global variables for validation scanner
observer = UnifiedStatisticalNexus()
plugin_observer = observer

if __name__ == "__main__":
    # Baseline framework execution verification
    mock_payload = "Evaluating normal distribution variance and bayesian posterior bounds."
    observer.evaluate(0.85, 0.90, 0.50, [0.4, 0.5, 0.45, 0.55], text=mock_payload, haptic_level=0.1)