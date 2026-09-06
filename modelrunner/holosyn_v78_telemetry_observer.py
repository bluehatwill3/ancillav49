#!/usr/bin/env python3
"""
HOLOSYN V78: MASTER HARDWARE TELEMETRY & OS RESOURCE NEXUS
===================================================================================
Hardware Target: Dell Latitude 5420 (i5-1145G7 | 16GB RAM | CPU-Only)
Role: Models OS-Level CPU Load, RAM Saturation, and Thermal Throttling.
Integration: Fuses psutil OS hooks with Qwen 0.5B Symbolic Hardware Diagnostics.
"""

import sys
import os
import gc
import torch
import torch.nn as nn
import numpy as np
import warnings
import re
import time

try:
    import psutil
    PSUTIL_AVAILABLE = True
except ImportError:
    PSUTIL_AVAILABLE = False

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
            print(f"   🧬 [TELEMETRY CORE] Hardware baseline weights mapped from: {os.path.basename(path)}")
            return True
        except Exception: return False


# ──────────────────────────────────────────────────────────────────────
# 🖥️ OS HARDWARE TELEMETRY SCANNER
# ──────────────────────────────────────────────────────────────────────
class OSTelemetryScanner:
    """
    Directly queries the host Operating System for physical hardware metrics.
    Handles CPU utilization, Memory pressure, and simulated thermal buildup.
    """
    def __init__(self):
        self.psutil_active = PSUTIL_AVAILABLE
        self.historical_cpu = 0.5
        self.thermal_proxy = 0.0
        
        if not self.psutil_active:
            print("   ⚠️ [TELEMETRY] 'psutil' missing. Falling back to surrogate hardware heuristics.")

    def fetch_hardware_metrics(self, s, haptic_level):
        cpu_load = 0.5
        ram_sat = 0.5
        
        if self.psutil_active:
            try:
                # Non-blocking CPU check
                cpu_load = psutil.cpu_percent(interval=None) / 100.0
                mem = psutil.virtual_memory()
                ram_sat = mem.percent / 100.0
            except Exception:
                pass
        else:
            # Surrogate heuristics based on framework strain
            cpu_load = np.clip((1.0 - s) + (haptic_level * 0.5), 0.1, 0.99)
            ram_sat = 0.6 + (haptic_level * 0.2)
            
        # Smooth CPU load over time to represent sustained effort
        self.historical_cpu = (self.historical_cpu * 0.8) + (cpu_load * 0.2)
        
        # Thermal Proxy: If CPU is sustained > 80% and friction is high, heat builds up.
        if self.historical_cpu > 0.8:
            self.thermal_proxy = np.clip(self.thermal_proxy + 0.05, 0.0, 1.0)
        else:
            self.thermal_proxy = np.clip(self.thermal_proxy - 0.02, 0.0, 1.0)
            
        return float(cpu_load), float(ram_sat), float(self.thermal_proxy)


# ──────────────────────────────────────────────────────────────────────
# 🧠 HUGGINGFACE SYMBOLIC DIAGNOSTIC SWARM
# ──────────────────────────────────────────────────────────────────────
try:
    from transformers import AutoModelForCausalLM, AutoTokenizer
    HF_AVAILABLE = True
except ImportError:
    HF_AVAILABLE = False

class TelemetrySymbolicMicroSwarm:
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
            print(f"   ⏳ [DIAGNOSTIC MICROMODEL] Allocating {model_id} to CPU...")
            self.model = AutoModelForCausalLM.from_pretrained(model_id, torch_dtype=self.dtype).eval()
            self.tokenizer = AutoTokenizer.from_pretrained(model_id)
            self.active = True
            print("   ✅ [DIAGNOSTIC MICROMODEL] Symbolic Telemetry Engine Locked.")
        except Exception as e: 
            print(f"   ⚠️ [DIAGNOSTIC MICROMODEL] Model bypass active. {e}")

    def evaluate_system_health(self, cpu_load, ram_sat, thermal):
        if not self.active:
            return float(np.clip(1.0 - max(cpu_load, ram_sat, thermal), 0.0, 1.0))
            
        prompt = f"Hardware Vitals: CPU Load = {cpu_load*100:.1f}%. RAM Saturation = {ram_sat*100:.1f}%. Thermal Throttling Proxy = {thermal:.2f}. Is the host system physically stable and capable of sustained operations? Output only a float between 0.0 (Failing/Critical) and 1.0 (Healthy/Optimal)."
        try:
            inputs = self.tokenizer(prompt, return_tensors="pt")
            with torch.no_grad():
                outputs = self.model.generate(**inputs, max_new_tokens=10, do_sample=False)
            response = self.tokenizer.decode(outputs[0][inputs.input_ids.size(1):], skip_special_tokens=True)
            match = re.search(r"0\.\d+|1\.0", response)
            if match: return float(match.group())
            return float(np.clip(1.0 - cpu_load, 0.0, 1.0))
        except Exception: 
            return 0.5


# ──────────────────────────────────────────────────────────────────────
# 🌐 MASTER TELEMETRY NEXUS ORCHESTRATOR
# ──────────────────────────────────────────────────────────────────────
class UnifiedTelemetryNexus(BaseObserver):
    def __init__(self):
        super().__init__()
        print("💠 [TELEMETRY NEXUS] Initializing OS-Level Hardware Diagnostics...")
        
        self.hive_core = HiveFusionCore().eval()
        self._bind_master_weights()
        
        self.scanner = OSTelemetryScanner()
        self.symbolic_engine = TelemetrySymbolicMicroSwarm()

    def _bind_master_weights(self):
        locations = ["hive_fused_all.pt", "hive_best.pt", "/home/devcbloom/Downloads/hive_fused_all.pt"]
        for path in locations:
            if self.hive_core.assimilate_hive(path):
                break

    def evaluate(self, s, sy, p, snn, text="", haptic_level=0.0, **kwargs):
        
        # 1. Fetch raw OS physical telemetry
        cpu_load, ram_sat, thermal_proxy = self.scanner.fetch_hardware_metrics(s, haptic_level)
        
        # 2. Evaluate Symbolic Hardware Health using HuggingFace Micro-Model
        symbolic_health = self.symbolic_engine.evaluate_system_health(cpu_load, ram_sat, thermal_proxy)
        
        # 3. Calculate Hardware Overload Factor (Used to throttle the system if physically failing)
        hardware_stability = 1.0 - max(cpu_load, ram_sat, thermal_proxy)
        throttle_factor = np.clip(hardware_stability + 0.2, 0.1, 1.0) # Allows some buffer before total throttling
        
        # Record into framework pipeline
        kwargs['os_cpu_load'] = cpu_load
        kwargs['os_ram_sat'] = ram_sat
        kwargs['os_thermal_proxy'] = thermal_proxy
        kwargs['os_throttle_factor'] = throttle_factor  # Hardware constraint modifier
        
        print(f"   🖥️ [OS TELEMETRY] CPU: {cpu_load*100:.1f}% | RAM: {ram_sat*100:.1f}% | Thermal Proxy: {thermal_proxy:.2f}")
        print(f"   🤖 [SYMBOLIC HARDWARE HEALTH]: {symbolic_health:.4f}")

        try:
            snn_density = float(np.mean(snn)) if (snn is not None and hasattr(snn, '__len__') and len(snn) > 0) else 0.5
            
            # Vector allocation: [Coherence, CPU Inverse, RAM Inverse, SNN Density, Symbolic Health]
            state_matrix = torch.tensor([[[s, (1.0 - cpu_load), (1.0 - ram_sat), snn_density, symbolic_health]]], dtype=torch.float32)
            
            with torch.no_grad():
                master_judgment = self.hive_core(state_matrix).item()
        except Exception:
            master_judgment = 0.5

        # Compile final unified telemetry resonance
        final_resonance = np.clip((symbolic_health * 0.4) + (master_judgment * 0.6), 0.0, 1.0)
        
        # THROTTLE APPLICATION: Suppress resonance if the host machine is physically melting down
        final_resonance = final_resonance * throttle_factor
        
        print(f"📊 [TELEMETRY NEXUS TOTAL RESONANCE (Throttled)]: {final_resonance:.4f}")
        print("═" * 80)
        return float(final_resonance)


# Register global variables for strict validation scanner checks
observer = UnifiedTelemetryNexus()
plugin_observer = observer

if __name__ == "__main__":
    # Baseline framework execution verification
    observer.evaluate(0.90, 0.95, 0.50, [0.3, 0.4, 0.5], text="Telemetry ping.", haptic_level=0.1)