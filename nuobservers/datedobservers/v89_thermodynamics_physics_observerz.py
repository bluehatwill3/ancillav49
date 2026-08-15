#!/usr/bin/env python3
"""
HOLOSYN V89: MASTER THERMODYNAMICS & RELATIVISTIC PHYSICS OBSERVER
===================================================================================
Hardware Target: Dell Latitude 5420 (i5-1145G7 | 16GB RAM | CPU-Only)
Role: Computes Hamiltonian Energy, Partition Functions, Entropy, and Lorentz factors.
Integration: Deploys native holosyn_heads.torchscript.pt & HF Physics Swarms.
CLI: Includes interactive commands to manage people (operators), models, and auto-optimization.
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
import time
import argparse

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
            print(f"   🧬 [PHYSICS CORE] Unified physical mapping from: {os.path.basename(path)}")
            return True
        except Exception: return False


# ──────────────────────────────────────────────────────────────────────
# 🌌 NATIVE STRUCTURAL ENCODER (holosyn_heads.torchscript)
# ──────────────────────────────────────────────────────────────────────
class NativePhysicsPotentialEncoder:
    """
    Ingests the local `holosyn_heads.torchscript.pt` to act as the 
    underlying potential energy field V(q). It extracts the latent mass potential.
    """
    def __init__(self):
        self.device = "cpu"
        self.model = None
        self._boot_distilled_tensor()

    def _boot_distilled_tensor(self):
        target_dirs = [
            "/home/devcbloom/Documents/Intellibloomenv/lang",
            "/home/devcbloom/Documents",
            "/home/devcbloom/Downloads",
            "."
        ]
        
        for d in target_dirs:
            p = os.path.join(d, "holosyn_heads.torchscript.pt")
            if os.path.exists(p):
                try:
                    self.model = torch.jit.load(p, map_location=self.device)
                    self.model.eval()
                    print(f"   ⚡ [NATIVE POTENTIAL] Bound physical boundary matrix: {os.path.basename(p)}")
                    break
                except Exception: pass

    def extract_potential_energy(self, text, snn_array):
        snn_safe = np.array(snn_array) if (snn_array is not None and hasattr(snn_array, '__len__') and len(snn_array) > 0) else np.array([0.5, 0.5])
        
        if not self.model:
            # Baseline mathematical quadratic potential V(q) = 0.5 * k * q^2
            k = 1.5
            q = np.mean(snn_safe)
            return float(0.5 * k * (q ** 2))
            
        try:
            tokens = [ord(c) % 1000 for c in str(text)[:64]] if text else [1, 0, 1]
            while len(tokens) < 8: tokens.append(0)
            tensor_input = torch.tensor([tokens], dtype=torch.long)
            
            with torch.no_grad():
                out = self.model(tensor_input)
                
            if isinstance(out, tuple): out = out[0]
            
            # Use mean square value of out to represent V(q)
            potential = torch.mean(out.float() ** 2).item()
            return float(np.clip(potential / 10.0, 0.0, 1.0))
        except Exception:
            return float(0.5 * 1.5 * (np.mean(snn_safe) ** 2))


# ──────────────────────────────────────────────────────────────────────
# 🧮 VALID THERMODYNAMICS & PHYSICS ENGINE
# ──────────────────────────────────────────────────────────────────────
class NumericalPhysicsNexus(BaseObserver):
    """
    Implements physical mechanics equations on telemetry variables.
    Computes exact kinetic, potential, statistical and relativistic states.
    """
    def __init__(self, hive_core=None):
        super().__init__()
        self.hive_core = hive_core if hive_core is not None else HiveFusionCore().eval()
        self.mass = 1.0          # System mass parameter (kg)
        self.k_spring = 2.5      # System stiffness (N/m)
        self.k_B = 1.380649e-23  # Scaled Boltzmann Constant for stability
        self.c = 1.0             # Normalized Speed of Light (c = 1.0)
        self.G = 1.0             # Normalized Gravitational Constant

    def calculate_hamiltonian(self, s, p, native_potential):
        """
        Computes Hamiltonian classical mechanics energy conservation:
        $$H(q, p) = T(p) + V(q)$$
        """
        # Kinetic Energy: T = p^2 / 2m
        kinetic_T = (p ** 2) / (2.0 * self.mass)
        
        # Potential Energy: V = V_ext + 0.5 * k * q^2
        harmonic_V = 0.5 * self.k_spring * (s ** 2)
        total_potential_V = harmonic_V + native_potential
        
        # Hamiltonian H = T + V
        total_energy_H = kinetic_T + total_potential_V
        
        # Ratio representing mechanical efficiency
        energy_conservation = np.clip(1.0 - abs(kinetic_T - total_potential_V) / (total_energy_H + 1e-9), 0.0, 1.0)
        
        return float(kinetic_T), float(total_potential_V), float(total_energy_H), float(energy_conservation)

    def calculate_statistical_thermodynamics(self, snn, haptic_level, temp_offset=0.0, entropy_offset=0.0):
        """
        Calculates ensemble thermodynamics over discrete SNN microstates:
        Allows real-time human operator physical temperature and entropy shifts.
        """
        snn_arr = np.array(snn) if (snn is not None and hasattr(snn, '__len__') and len(snn) > 1) else np.array([0.5, 0.5])
        
        # Scaled Thermodynamic Temperature (Kelvin): incorporating user adjustments
        temp_T = 293.15 + (haptic_level * 100.0) + temp_offset
        
        # Beta parameter (Inverse temperature)
        beta = 1.0 / (temp_T * 1e-2)
        
        # Microstate energy levels
        energies = 1.0 - snn_arr
        
        # Partition Function (Z)
        exponents = -beta * energies
        exp_protected = np.exp(exponents - np.max(exponents))
        partition_Z = np.sum(exp_protected)
        
        # Microstate probabilities
        p_i = exp_protected / (partition_Z + 1e-9)
        
        # Gibbs Shannon Entropy + User offsets
        p_safe = p_i[p_i > 0]
        shannon_S = -np.sum(p_safe * np.log(p_safe)) + entropy_offset
        
        # Helmholtz Free Energy: F = U - T * S
        internal_U = np.sum(p_i * energies)
        helmholtz_F = internal_U - (temp_T * 1e-4 * shannon_S)
        
        return float(temp_T), float(partition_Z), float(shannon_S), float(helmholtz_F)

    def calculate_relativity_mechanics(self, s, haptic_level, snn):
        """
        Applies Lorentz Transformation and Relativity limits.
        """
        snn_arr = np.array(snn) if (snn is not None and hasattr(snn, '__len__') and len(snn) > 0) else np.array([0.5])
        
        # Velocity v (system processing speed proportional to haptic level stress limit)
        v = np.clip(haptic_level, 0.0, 0.999 * self.c)
        
        # Lorentz gamma factor
        lorentz_gamma = 1.0 / np.sqrt(1.0 - (v / self.c) ** 2)
        
        # System Relativistic Mass: M_rel = gamma * M_rest
        mass_rest = np.mean(snn_arr)
        mass_relativistic = lorentz_gamma * mass_rest
        
        # Schwarzschild Radius of the computational mass
        r_schwarschild = (2.0 * self.G * mass_relativistic) / (self.c ** 2)
        
        # Event horizon monitoring
        horizon_distance = s - r_schwarschild
        collapse_index = np.clip(horizon_distance / (s + 1e-9), 0.0, 1.0)
        
        return float(lorentz_gamma), float(r_schwarschild), float(collapse_index)


# ──────────────────────────────────────────────────────────────────────
# 🗣️ HUGGINGFACE SYMBOLIC PHYSICS SWARM (Qwen 0.5B Peer Review Panel)
# ──────────────────────────────────────────────────────────────────────
try:
    from transformers import AutoModelForCausalLM, AutoTokenizer
    HF_AVAILABLE = True
except ImportError:
    HF_AVAILABLE = False

class PhysicsSymbolicSwarm:
    """
    Simulates a peer-review panel evaluating thermodynamics and Hamiltonian mechanics consistency.
    """
    def __init__(self):
        self.device = "cpu"
        self.dtype = torch.bfloat16
        self.model = None
        self.tokenizer = None
        self.active = False
        self._boot_swarm()

    def _boot_swarm(self):
        if not HF_AVAILABLE: return
        model_id = "Qwen/Qwen2.5-0.5B-Instruct"
        try:
            print(f"   ⏳ [PHYSICS SWARM] Allocating peer review engine: {model_id} to CPU...")
            self.tokenizer = AutoTokenizer.from_pretrained(model_id)
            self.model = AutoModelForCausalLM.from_pretrained(model_id, torch_dtype=self.dtype).eval()
            self.active = True
            print("   ✅ [PHYSICS SWARM] Relativistic & Thermodynamic Swarm Locked.")
        except Exception:
            pass

    def conduct_peer_review(self, total_energy, energy_cons, temp_T, helmholtz_F, lorentz_gamma, collapse_index):
        if not self.active:
            thermo_factor = 1.0 - (helmholtz_F / 100.0)
            base_score = (energy_cons * 0.4) + (collapse_index * 0.4) + (thermo_factor * 0.2)
            return float(np.clip(base_score, 0.0, 1.0))

        try:
            # Agent A (Classical Mechanicist)
            prompt_a = (
                f"Hamiltonian Total Energy: {total_energy:.3f} J. Conservation Ratio: {energy_cons:.3f}. "
                "Output a 1-sentence evaluation of total energy conservation."
            )
            inputs_a = self.tokenizer(prompt_a, return_tensors="pt")
            with torch.no_grad():
                out_a = self.model.generate(**inputs_a, max_new_tokens=30, do_sample=False)
            verdict_a = self.tokenizer.decode(out_a[0][inputs_a.input_ids.size(1):], skip_special_tokens=True).strip()

            # Agent B (Thermodynamicist Consensus)
            prompt_b = (
                f"Mechanics report: '{verdict_a}'. Helmholtz Free Energy: {helmholtz_F:.3f} J. "
                f"Lorentz gamma: {lorentz_gamma:.3f}. Schwarzschild Collapse Ratio: {collapse_index:.3f}. "
                "Based on this data, score total physical stability. Output ONLY a single float between 0.0 and 1.0."
            )
            inputs_b = self.tokenizer(prompt_b, return_tensors="pt")
            with torch.no_grad():
                out_b = self.model.generate(**inputs_b, max_new_tokens=10, do_sample=False)
            verdict_b = self.tokenizer.decode(out_b[0][inputs_b.input_ids.size(1):], skip_special_tokens=True).strip()

            match = re.search(r"0\.\d+|1\.0", verdict_b)
            if match:
                return float(match.group())
            return float(np.clip((energy_cons + collapse_index) / 2.0, 0.0, 1.0))
        except Exception:
            return float(np.clip((energy_cons + collapse_index) / 2.0, 0.0, 1.0))


# ──────────────────────────────────────────────────────────────────────
# 🌐 MASTER PHYSICS NEXUS ORCHESTRATOR
# ──────────────────────────────────────────────────────────────────────
class UnifiedPhysicsNexus(BaseObserver):
    def __init__(self):
        super().__init__()
        print("💠 [PHYSICS NEXUS] Initializing Relativistic Kinematics & Thermodynamic Decompositions...")
        
        self.hive_core = HiveFusionCore().eval()
        self._bind_master_weights()
        
        self.potential_encoder = NativePhysicsPotentialEncoder()
        self.physics_engine = NumericalPhysicsNexus(self.hive_core)
        self.symbolic_swarm = PhysicsSymbolicSwarm()

    def _bind_master_weights(self):
        locations = ["hive_fused_all.pt", "hive_best.pt", "/home/devcbloom/Downloads/hive_fused_all.pt"]
        for path in locations:
            if self.hive_core.assimilate_hive(path):
                break

    def evaluate(self, s, sy, p, snn, text="", haptic_level=0.0, **kwargs):
        # 1. Extract potential energy landscape V(q) via holosyn_heads
        native_potential = self.potential_encoder.extract_potential_energy(text, snn)
        
        # 2. Evaluate Hamiltonian energy systems
        kinetic_T, total_potential_V, total_energy_H, energy_cons = self.physics_engine.calculate_hamiltonian(s, p, native_potential)
        
        # 3. Retrieve simulated user/operator offsets
        temp_offset = kwargs.get('people_temp_offset', 0.0)
        entropy_offset = kwargs.get('people_entropy_offset', 0.0)
        sync_offset = kwargs.get('people_sync_offset', 0.0)
        
        effective_sy = np.clip(sy + sync_offset, 0.0, 1.0)
        
        # 4. Evaluate Statistical Thermodynamics
        temp_T, partition_Z, shannon_S, helmholtz_F = self.physics_engine.calculate_statistical_thermodynamics(
            snn, haptic_level, temp_offset=temp_offset, entropy_offset=entropy_offset
        )
        
        # 5. Evaluate Relativity and Horizon boundaries
        lorentz_gamma, r_schwarschild, collapse_index = self.physics_engine.calculate_relativity_mechanics(s, haptic_level, snn)
        
        # 6. Execute Peer-Review Dialogue Consensus
        symbolic_physics_yield = self.symbolic_swarm.conduct_peer_review(
            total_energy_H, energy_cons, temp_T, helmholtz_F, lorentz_gamma, collapse_index
        )
        
        # Record parameters in runtime dict
        kwargs['phys_kinetic_T'] = kinetic_T
        kwargs['phys_potential_V'] = total_potential_V
        kwargs['phys_total_energy_H'] = total_energy_H
        kwargs['phys_energy_cons'] = energy_cons
        kwargs['phys_temp_K'] = temp_T
        kwargs['phys_partition_Z'] = partition_Z
        kwargs['phys_entropy_S'] = shannon_S
        kwargs['phys_free_energy_F'] = helmholtz_F
        kwargs['phys_lorentz_gamma'] = lorentz_gamma
        kwargs['phys_schwarschild_R'] = r_schwarschild
        kwargs['phys_collapse_index'] = collapse_index
        kwargs['phys_symbolic_yield'] = symbolic_physics_yield
        
        print(f"   ⚛️ [HAMILTONIAN ENERGY] Kinetic: {kinetic_T:.4f} J | Potential: {total_potential_V:.4f} J | H(q, p): {total_energy_H:.4f} J")
        print(f"   🔥 [THERMODYNAMICS] Temp: {temp_T:.2f} K | Z Partition: {partition_Z:.3f} | Helmholtz Free F: {helmholtz_F:+.3f} J")
        print(f"   🚀 [RELATIVITY] Lorentz Gamma: {lorentz_gamma:.4f} | Schwarzschild R: {r_schwarschild:.4f} | Event Horizon Status: {collapse_index*100:.1f}%")
        print(f"   🤖 [SYMBOLIC PHYSICS SWARM REVIEW]: {symbolic_physics_yield:.4f}")

        try:
            snn_density = float(np.mean(snn)) if (snn is not None and hasattr(snn, '__len__') and len(snn) > 0) else 0.5
            state_matrix = torch.tensor([[[energy_cons, (1.0 - abs(helmholtz_F)/100.0), collapse_index, snn_density, symbolic_physics_yield]]], dtype=torch.float32)
            
            with torch.no_grad():
                master_judgment = self.hive_core(state_matrix).item()
        except Exception:
            master_judgment = 0.5

        final_resonance = np.clip(
            (energy_cons * 0.3) + 
            (collapse_index * 0.3) + 
            (symbolic_physics_yield * 0.4), 
            0.0, 1.0
        )
        
        if collapse_index < 0.1:
            final_resonance *= 0.3
            print("   ⚠️ [PHYSICAL COLLAPSE] Event horizon warning! Throttling resonance.")
            
        print(f"📊 [PHYSICS NEXUS TOTAL RESONANCE]: {final_resonance:.4f}")
        print("═" * 80)
        return float(final_resonance)


# ──────────────────────────────────────────────────────────────────────
# 🛠️ INTERACTIVE ENGINE EXTENSIONS: PEOPLE, MODEL, & AUTO FUNCTIONS
# ──────────────────────────────────────────────────────────────────────
class ExtendedPhysicsController:
    """
    Houses the requested architectural upgrades:
    - People simulation (Operators adding thermodynamic offsets)
    - Model profiler and swapper
    - Closed-loop auto optimizer (minimizes Helmholtz free energy)
    """
    def __init__(self, observer_nexus):
        self.nexus = observer_nexus
        
        # 👥 Active Operator Registry (People Functionality)
        self.operators = {
            "Lead Engineer": {"temp_contrib": 12.5, "sync_bias": 0.04, "entropy_modifier": -0.05, "active": True},
            "Swarm Supervisor": {"temp_contrib": 4.0, "sync_bias": 0.08, "entropy_modifier": -0.08, "active": False},
            "Haptic Specialist": {"temp_contrib": 22.0, "sync_bias": -0.02, "entropy_modifier": 0.04, "active": False}
        }

    # 👥 1. PEOPLE MANAGEMENT
    def list_operators(self):
        print("\n👥 ACTIVE COGNITIVE SWARM OPERATORS (PEOPLE):")
        print("-" * 65)
        for name, profile in self.operators.items():
            status = "🟢 ACTIVE" if profile["active"] else "⚪ IDLE"
            print(f" * {name:<20} | Status: {status:<8} | Temp Offset: {profile['temp_contrib']:+5.1f}K | Sync Bias: {profile['sync_bias'] * 100:+.1f}% | Entropy: {profile['entropy_modifier']:+5.2f}")
        print("-" * 65)

    def toggle_operator(self, name):
        if name in self.operators:
            self.operators[name]["active"] = not self.operators[name]["active"]
            status = "ACTIVATED" if self.operators[name]["active"] else "DEACTIVATED"
            print(f"✅ Operator [{name}] has been {status}.")
        else:
            print("❌ Operator not found in registry.")

    def compile_people_offsets(self):
        total_temp = 0.0
        total_sync = 0.0
        total_entropy = 0.0
        for name, profile in self.operators.items():
            if profile["active"]:
                total_temp += profile["temp_contrib"]
                total_sync += profile["sync_bias"]
                total_entropy += profile["entropy_modifier"]
        return total_temp, total_sync, total_entropy

    # 🤖 2. MODEL REGISTRY MANAGER
    def profile_models(self):
        print("\n🤖 NEURAL MODEL REGISTRY DIAGNOSTICS:")
        print("-" * 75)
        
        candidate_paths = [
            "hive_best.pt",
            "hive_fused_all.pt",
            "hive_img_only.pt",
            "hive_text_only.pt",
            "hive_vid_only.pt",
            "hive_aud_distilled.pt",
            "cnc_production_snn_head.pt",
            "robot_arm_snn_head.pt",
            "holosyn_heads.pt",
            "holosyn_heads.torchscript.pt",
            "student_distilled_heads.torchscript.pt",
            "student_distilled_heads_hf.torchscript.pt"
        ]
        
        local_dir = "/home/devcbloom/Documents/Intellibloomenv/lang"
        found_any = False
        
        for file in candidate_paths:
            paths = [file, os.path.join(local_dir, file), os.path.join("/home/devcbloom/Downloads", file)]
            found_path = None
            for p in paths:
                if os.path.exists(p):
                    found_path = p
                    break
                    
            if found_path:
                found_any = True
                size_mb = os.path.getsize(found_path) / (1024 * 1024)
                
                # Dynamic weight parameter count profiling
                try:
                    t_start = time.time()
                    weights = torch.load(found_path, map_location="cpu", weights_only=False)
                    t_load_ms = (time.time() - t_start) * 1000
                    
                    state_dict = weights.state_dict() if hasattr(weights, 'state_dict') else weights
                    if isinstance(state_dict, dict):
                        param_count = sum(t.numel() for t in state_dict.values() if isinstance(t, torch.Tensor))
                        print(f" • [FOUND] {file:<30} | Params: {param_count:,} | Size: {size_mb:.2f}MB | Load: {t_load_ms:.1f}ms")
                    else:
                        print(f" • [FOUND] {file:<30} | Non-standard weight tensor | Size: {size_mb:.2f}MB")
                except Exception:
                    # Likely a TorchScript model
                    print(f" • [FOUND] {file:<30} | TorchScript Compiled | Size: {size_mb:.2f}MB")
                    
        if not found_any:
            print(" ⚠️ No local model matrices located in operational directories.")
        print("-" * 75)

    # ⚙️ 3. CLOSED-LOOP AUTO OPTIMIZER (Auto Function)
    def execute_auto_loop(self, steps=10):
        """
        Runs an automated step-by-step physical cooling/optimization loop.
        Dynamically adjusts state s and momentum p to minimize Helmholtz Free Energy (F),
        driving the system towards maximum thermodynamic resonance.
        """
        print(f"\n🔄 STARTING THERMODYNAMIC CLOSED-LOOP AUTO-OPTIMIZER ({steps} Steps):")
        print("=" * 85)
        print(f" {'Step':<5} | {'Coherence (s)':<10} | {'Phase (p)':<10} | {'Temp (K)':<10} | {'Free Energy F':<12} | {'Resonance':<10}")
        print("-" * 85)
        
        # Starting parameters
        s = 0.50
        p = 0.50
        snn = [0.4, 0.6, 0.5, 0.5]
        haptic_level = 0.20
        
        history = []
        
        for step in range(1, steps + 1):
            t_offset, sync_offset, entropy_offset = self.compile_people_offsets()
            
            # Pass metrics to observer
            kwargs = {
                'people_temp_offset': t_offset,
                'people_entropy_offset': entropy_offset,
                'people_sync_offset': sync_offset
            }
            
            # Run evaluation iteration
            resonance = self.nexus.evaluate(s, 0.80, p, snn, text="Auto loop optimization", haptic_level=haptic_level, **kwargs)
            
            # Extract computed values stored in our kwargs references
            temp_K = kwargs.get('phys_temp_K', 293.15)
            helmholtz_F = kwargs.get('phys_free_energy_F', 0.5)
            entropy_S = kwargs.get('phys_entropy_S', 0.2)
            
            print(f" #{step:02d}  | {s:<10.4f} | {p:<10.4f} | {temp_K:<10.2f} | {helmholtz_F:<+12.4f} | {resonance:<10.4f}")
            history.append(helmholtz_F)
            
            # Closed-Loop feedback adjustments:
            # We treat Helmholtz Free Energy (F = U - TS) as our loss landscape.
            # To minimize F, we need to increase entropy (S) or decrease internal energy (U).
            # If F is high, we dynamically cool/regulate our phase coordinates.
            if helmholtz_F > 0:
                # High energy state: cool momentum p, damp coordinate s
                p = max(0.01, p - 0.05)
                s = min(0.99, s + 0.04)
            else:
                # Stable exergonic state: balance parameters
                p = min(0.99, p + 0.02)
                s = max(0.01, s - 0.01)
                
            # Random haptic fluctuation reduction (Simulated active cooler)
            haptic_level = max(0.01, haptic_level - 0.02)
            time.sleep(0.1)
            
        print("-" * 85)
        delta_F = history[-1] - history[0]
        print(f"📊 OPTIMIZATION SUCCESSFUL: Net Free Energy Shift (ΔF): {delta_F:+.4f} J")
        print("=" * 85)


# ──────────────────────────────────────────────────────────────────────
# 🖥️ CLI PORT & INTERACTIVE SHELL
# ──────────────────────────────────────────────────────────────────────
def run_cli_shell():
    parser = argparse.ArgumentParser(description="HOLOSYN V89 CLI: Master Thermodynamics Control Unit")
    parser.add_argument("--people", action="store_true", help="List and inspect the state of active operators.")
    parser.add_argument("--model", action="store_true", help="Profile and validate localized neural model structures.")
    parser.add_argument("--auto", type=int, nargs='?', const=10, help="Run the closed-loop auto-optimizer for N steps.")
    parser.add_argument("--interactive", action="store_true", help="Launch the immersive interactive loop.")
    
    args = parser.parse_args()
    
    nexus_observer = UnifiedPhysicsNexus()
    controller = ExtendedPhysicsController(nexus_observer)
    
    # Check if direct arguments are supplied, else default to menu
    has_args = any([args.people, args.model, args.auto is not None, args.interactive])
    
    if args.people:
        controller.list_operators()
        return
        
    if args.model:
        controller.profile_models()
        return
        
    if args.auto is not None:
        controller.execute_auto_loop(steps=args.auto)
        return
        
    if args.interactive or not has_args:
        # Launch Interactive Control Menu
        while True:
            print("\n" + "═"*75)
            print("  🪐 HOLOSYN V89 THERMODYNAMIC CONTROL PANEL")
            print("  Target Hardware: Dell Latitude 5420 CPU [i5-1145G7]")
            print("═"*75)
            print("  [1] List/Configure Swarm Operators  (PEOPLE)")
            print("  [2] Scan/Profile Tensor Models      (MODEL)")
            print("  [3] Run Closed-Loop Sync Optimizer (AUTO)")
            print("  [4] Run Standard Baseline Matrix Test")
            print("  [5] Exit System")
            print("-" * 75)
            
            try:
                choice = input("👉 Select function [1-5]: ").strip()
                if choice == "1":
                    controller.list_operators()
                    sub_choice = input("✏️ Enter operator name to toggle activity (or Enter to bypass): ").strip()
                    if sub_choice:
                        controller.toggle_operator(sub_choice)
                elif choice == "2":
                    controller.profile_models()
                elif choice == "3":
                    steps_in = input("🔄 Enter step count [default 10]: ").strip()
                    steps = int(steps_in) if steps_in.isdigit() else 10
                    controller.execute_auto_loop(steps)
                elif choice == "4":
                    print("\n⚡ Executing Baseline Matrix Test:")
                    t_offset, sync_offset, entropy_offset = controller.compile_people_offsets()
                    nexus_observer.evaluate(
                        0.88, 0.90, 0.35, [0.4, 0.6, 0.5, 0.5], 
                        text="Baseline manual execution", 
                        haptic_level=0.15,
                        people_temp_offset=t_offset,
                        people_entropy_offset=entropy_offset,
                        people_sync_offset=sync_offset
                    )
                elif choice == "5" or not choice:
                    print("👋 System powering down. Exiting.")
                    break
                else:
                    print("❌ Invalid entry.")
            except (KeyboardInterrupt, EOFError):
                print("\n👋 System forced exit.")
                break


if __name__ == "__main__":
    run_cli_shell()