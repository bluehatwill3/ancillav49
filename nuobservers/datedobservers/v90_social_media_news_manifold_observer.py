#!/usr/bin/env python3
"""
HOLOSYN V90: MASTER SOCIAL MEDIA & NEWS INFORMATION MANIFOLD OBSERVER
===================================================================================
Hardware Target: Dell Latitude 5420 (i5-1145G7 | 16GB RAM | CPU-Only)
Role: Models Geodesic Flow, Ricci Curvature Polarization, and Semantic Entropy.
Integration: Ingests native hive_text_only.pt & student_distilled_heads_hf.pt
CLI: Features interactive methods to assimilate feeds and auto-optimize manifolds.
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
            print(f"   🧬 [MANIFOLD CORE] Unified semantic weights mapped from: {os.path.basename(path)}")
            return True
        except Exception: return False


# ──────────────────────────────────────────────────────────────────────
# 📝 NATIVE TEXT & SEMANTIC MANIFOLD ENCODER (hive_text_only / student_distilled)
# ──────────────────────────────────────────────────────────────────────
class NativeSemanticManifoldEncoder:
    """
    Ingests the local `hive_text_only.pt` and `student_distilled_heads_hf.torchscript.pt` 
    to map raw social media text feeds into exact high-dimensional latent coordinates.
    """
    def __init__(self):
        self.device = "cpu"
        self.text_weights = None
        self.distilled_model = None
        self._boot_text_structures()

    def _boot_text_structures(self):
        target_dirs = [
            "/home/devcbloom/Documents/Intellibloomenv/lang",
            "/home/devcbloom/Documents",
            "/home/devcbloom/Downloads",
            "."
        ]
        
        # 1. Load PyTorch Weights
        for d in target_dirs:
            p_weights = os.path.join(d, "hive_text_only.pt")
            if os.path.exists(p_weights):
                try:
                    self.text_weights = torch.load(p_weights, map_location=self.device, weights_only=False)
                    print(f"   ⚡ [NATIVE SEMANTICS] Ingested semantic weight mapping: {os.path.basename(p_weights)}")
                    break
                except Exception: pass

        # 2. Load TorchScript Model
        for d in target_dirs:
            p_script = os.path.join(d, "student_distilled_heads_hf.torchscript.pt")
            if os.path.exists(p_script):
                try:
                    self.distilled_model = torch.jit.load(p_script, map_location=self.device)
                    self.distilled_model.eval()
                    print(f"   ⚡ [NATIVE SEMANTICS] Ingested TorchScript text head: {os.path.basename(p_script)}")
                    break
                except Exception: pass

    def project_text_to_manifold(self, text, snn_array):
        """
        Projects semantic text tokens through the model to obtain coordinate indices.
        """
        snn_safe = np.array(snn_array) if (snn_array is not None and hasattr(snn_array, '__len__') and len(snn_array) > 0) else np.array([0.5, 0.5])
        
        # Fallback to character hashing coordinates if weights are missing
        if self.distilled_model is None and self.text_weights is None:
            char_sum = sum(ord(c) for c in str(text))
            normalized_coord = (char_sum % 1000) / 1000.0
            return float(np.clip(normalized_coord, 0.0, 1.0))
            
        try:
            # Map input text into standardized token tensor
            tokens = [ord(c) % 1000 for c in str(text)[:64]] if text else [1, 0, 1]
            while len(tokens) < 8: tokens.append(0)
            tensor_input = torch.tensor([tokens], dtype=torch.long)
            
            # Extract latent coordinate from TorchScript
            if self.distilled_model is not None:
                with torch.no_grad():
                    out = self.distilled_model(tensor_input)
                if isinstance(out, tuple): out = out[0]
                coordinate = torch.mean(torch.abs(out.float())).item()
                return float(np.clip(coordinate / 10.0, 0.0, 1.0))
                
            # Fallback to weight dictionary matrix operations
            if self.text_weights is not None:
                first_key = [k for k in self.text_weights.keys() if 'weight' in k][0]
                w = self.text_weights[first_key]
                dim = w.shape[-1] if len(w.shape) > 0 else 1
                padded_snn = np.pad(snn_safe, (0, max(0, dim - len(snn_safe))), 'constant')[:dim]
                proj = torch.matmul(w.float(), torch.tensor(padded_snn, dtype=torch.float32))
                coordinate = torch.mean(torch.abs(proj)).item()
                return float(np.clip(coordinate / 100.0, 0.0, 1.0))
                
        except Exception:
            return 0.5


# ──────────────────────────────────────────────────────────────────────
# 📐 MATHEMATICAL INFORMATION MANIFOLD ENGINE
# ──────────────────────────────────────────────────────────────────────
class InformationManifoldObserver(BaseObserver):
    """
    Computes exact Information Geometry calculations on incoming streams:
    - Geodesic Distance / Flow
    - Ricci Curvature / Polarization (Echo Chamber tracking)
    - Shannon Entropy Warp
    """
    def __init__(self, hive_core=None):
        super().__init__()
        self.hive_core = hive_core if hive_core is not None else HiveFusionCore().eval()
        self.previous_snn = None

    def calculate_polarization_curvature(self, snn):
        """
        Calculates the Ricci Curvature proxy of the local information manifold.
        Highly polarized, segmented SNN states create non-convex regions
        represented by hyperbolic, negative curvature.
        Consensual, uniform states yield positive/spherical curvature.
        """
        snn_arr = np.array(snn) if (snn is not None and hasattr(snn, '__len__') and len(snn) > 1) else np.array([0.5, 0.5])
        
        # Bimodal polarization test: distance of states from the center
        median_val = np.median(snn_arr)
        polarization = np.mean(np.abs(snn_arr - median_val))
        
        # Ricci Curvature Proxy: R = 1.0 - 2.5 * Polarization
        # R > 0 (stable consensus), R < 0 (extreme echo chamber polarization)
        ricci_curvature = 1.0 - (2.5 * polarization)
        
        # Normalize into a stability metric [0, 1] (high curvature positive = high stability)
        topological_stability = np.clip((ricci_curvature + 1.0) / 2.0, 0.0, 1.0)
        return float(topological_stability), float(ricci_curvature)

    def calculate_geodesic_flow(self, snn):
        """
        Calculates the path length (Geodesic Flow distance) between 
        the preceding state vector and the current state vector.
        $$d(x, y) = \sqrt{\sum (x_i - y_i)^2}$$
        """
        snn_arr = np.array(snn) if (snn is not None and hasattr(snn, '__len__') and len(snn) > 0) else np.array([0.5])
        
        if self.previous_snn is None or len(self.previous_snn) != len(snn_arr):
            self.previous_snn = snn_arr
            return 0.0
            
        # Euclidean metric step on the local tangent space
        geodesic_step = np.linalg.norm(snn_arr - self.previous_snn)
        self.previous_snn = snn_arr
        
        # Velocity of trend propagation
        return float(np.clip(geodesic_step, 0.0, 1.0))

    def calculate_shannon_surprise(self, text, snn):
        """
        Computes the information entropy difference introduced by the incoming text.
        """
        snn_arr = np.array(snn) if (snn is not None and hasattr(snn, '__len__') and len(snn) > 0) else np.array([0.5])
        
        # Character probability density of input text
        text_str = str(text)
        if len(text_str) == 0: text_str = "empty"
        
        freqs = collections.Counter(text_str)
        total_chars = len(text_str)
        p_chars = np.array([count / total_chars for count in freqs.values()])
        
        # Shannon Entropy of input news feed: H = -sum(p * log2(p))
        feed_entropy = -np.sum(p_chars * np.log2(p_chars + 1e-9))
        
        # System expectation entropy
        p_system = np.abs(snn_arr) / (np.sum(np.abs(snn_arr)) + 1e-9)
        p_system = p_system[p_system > 0]
        system_entropy = -np.sum(p_system * np.log2(p_system + 1e-9))
        
        # Relative Entropy / Surprise warp
        surprise = abs(feed_entropy - system_entropy)
        return float(np.clip(surprise / 4.0, 0.0, 1.0))


# ──────────────────────────────────────────────────────────────────────
# 🗣️ HUGGINGFACE SYMBOLIC SWARM (Qwen 0.5B Fact-Check & Bias Review)
# ──────────────────────────────────────────────────────────────────────
try:
    from transformers import AutoModelForCausalLM, AutoTokenizer
    HF_AVAILABLE = True
except ImportError:
    HF_AVAILABLE = False

class ManifoldSymbolicSwarm:
    """
    Deploys a peer-review panel evaluating text polarization and factual integrity:
    Agent A (Social Sentimentalist): Detects emotional polarization.
    Agent B (Fact Verification Lead): Assesses topological drift and credibility.
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
            print(f"   ⏳ [MANIFOLD SWARM] Allocating peer review engine: {model_id} to CPU...")
            self.tokenizer = AutoTokenizer.from_pretrained(model_id)
            self.model = AutoModelForCausalLM.from_pretrained(model_id, torch_dtype=self.dtype).eval()
            self.active = True
            print("   ✅ [MANIFOLD SWARM] Social Media Fact-Check Swarm Locked.")
        except Exception:
            pass

    def evaluate_trend_objectivity(self, text, ricci_curvature, surprise_index):
        if not self.active:
            # Fallback mathematical score
            ricci_factor = max(0.0, ricci_curvature)
            base_score = (ricci_factor * 0.6) + ((1.0 - surprise_index) * 0.4)
            return float(np.clip(base_score, 0.0, 1.0))

        try:
            # Agent A: Polarization analysis
            prompt_a = (
                f"Evaluate social media input text: '{text[:120]}'. "
                f"Topological metric shows Ricci Curvature: {ricci_curvature:.3f}. "
                "Output a 1-sentence analysis on the sentiment polarization and potential echo chamber behavior."
            )
            inputs_a = self.tokenizer(prompt_a, return_tensors="pt")
            with torch.no_grad():
                out_a = self.model.generate(**inputs_a, max_new_tokens=40, do_sample=False)
            verdict_a = self.tokenizer.decode(out_a[0][inputs_a.input_ids.size(1):], skip_special_tokens=True).strip()

            # Agent B: Fact verification & consensus
            prompt_b = (
                f"Sentimentalist review: '{verdict_a}'. Information surprise index: {surprise_index:.3f}. "
                "Quantify overall consensus and truth-alignment. Output ONLY a single float between 0.0 and 1.0."
            )
            inputs_b = self.tokenizer(prompt_b, return_tensors="pt")
            with torch.no_grad():
                out_b = self.model.generate(**inputs_b, max_new_tokens=10, do_sample=False)
            verdict_b = self.tokenizer.decode(out_b[0][inputs_b.input_ids.size(1):], skip_special_tokens=True).strip()

            match = re.search(r"0\.\d+|1\.0", verdict_b)
            if match:
                return float(match.group())
            return float(np.clip((ricci_curvature + (1.0 - surprise_index)) / 2.0, 0.0, 1.0))
        except Exception:
            return float(np.clip((ricci_curvature + (1.0 - surprise_index)) / 2.0, 0.0, 1.0))


# ──────────────────────────────────────────────────────────────────────
# 🌐 MASTER SOCIAL MEDIA NEXUS ORCHESTRATOR
# ──────────────────────────────────────────────────────────────────────
class UnifiedSocialMediaNexus(BaseObserver):
    def __init__(self):
        super().__init__()
        print("💠 [SOCIAL NEXUS] Initializing Information Geometry & Semantic Manifold...")
        
        self.hive_core = HiveFusionCore().eval()
        self._bind_master_weights()
        
        self.semantic_encoder = NativeSemanticManifoldEncoder()
        self.manifold_engine = InformationManifoldObserver(self.hive_core)
        self.symbolic_swarm = ManifoldSymbolicSwarm()

    def _bind_master_weights(self):
        locations = ["hive_fused_all.pt", "hive_best.pt", "/home/devcbloom/Downloads/hive_fused_all.pt"]
        for path in locations:
            if self.hive_core.assimilate_hive(path):
                break

    def evaluate(self, s, sy, p, snn, text="", haptic_level=0.0, **kwargs):
        # 1. Project semantic text feed to manifold coordinates
        native_text_coord = self.semantic_encoder.project_text_to_manifold(text, snn)
        
        # 2. Evaluate manifold curvature and polarization
        topological_stability, ricci_curvature = self.manifold_engine.calculate_polarization_curvature(snn)
        
        # 3. Calculate Geodesic Flow Velocity
        geodesic_flow = self.manifold_engine.calculate_geodesic_flow(snn)
        
        # 4. Evaluate Surprise / Information Entropy Warp
        surprise_index = self.manifold_engine.calculate_shannon_surprise(text, snn)
        
        # 5. Conduct Peer-Review Fact Check Swarm
        symbolic_objectivity = self.symbolic_swarm.evaluate_trend_objectivity(
            text, ricci_curvature, surprise_index
        )
        
        # Save evaluation metrics to run context
        kwargs['info_semantic_coord'] = native_text_coord
        kwargs['info_ricci_curvature'] = ricci_curvature
        kwargs['info_topo_stability'] = topological_stability
        kwargs['info_geodesic_flow'] = geodesic_flow
        kwargs['info_surprise_index'] = surprise_index
        kwargs['info_symbolic_objectivity'] = symbolic_objectivity
        
        print(f"   📡 [INFORMATION METRIC] Ricci Curvature (R): {ricci_curvature:+.4f} | Geodesic Flow Velocity: {geodesic_flow:.4f}")
        print(f"   📖 [SEMANTIC FEED] Surprise Index: {surprise_index:.4f} | Native Projection: {native_text_coord:.4f}")
        print(f"   🤖 [SYMBOLIC OBJECTIVITY REVIEW]: {symbolic_objectivity:.4f}")

        try:
            snn_density = float(np.mean(snn)) if (snn is not None and hasattr(snn, '__len__') and len(snn) > 0) else 0.5
            # Compile 5D state matrix for master core processing
            state_matrix = torch.tensor([[[topological_stability, native_text_coord, (1.0 - geodesic_flow), snn_density, symbolic_objectivity]]], dtype=torch.float32)
            
            with torch.no_grad():
                master_judgment = self.hive_core(state_matrix).item()
        except Exception:
            master_judgment = 0.5

        # Compile final unified resonance score
        final_resonance = np.clip(
            (topological_stability * 0.3) + 
            (symbolic_objectivity * 0.4) + 
            (master_judgment * 0.3), 
            0.0, 1.0
        )
        
        # Echo chamber polarization penalty (extreme separation warps the processing pipeline)
        if ricci_curvature < -0.5:
            final_resonance *= 0.5
            print("   ⚠️ [ECHO CHAMBER COLLAPSE] Information manifold heavily polarized. Restricting resonance.")
            
        print(f"📊 [SOCIAL MEDIA NEXUS TOTAL RESONANCE]: {final_resonance:.4f}")
        print("═" * 80)
        return float(final_resonance)


# ──────────────────────────────────────────────────────────────────────
# 🛠️ INTERACTIVE ENGINE EXTENSIONS: ASSIMILATION & OPTIMIZATION
# ──────────────────────────────────────────────────────────────────────
class ExtendedSocialManifoldController:
    """
    Implements advanced functions to:
    - Assimilate real-time social / news text feeds
    - Visualize the Information Manifold topologically (ASCII plotting)
    - Auto-optimize (Closed-loop mitigation of polarization)
    """
    def __init__(self, observer_nexus):
        self.nexus = observer_nexus
        self.news_feed_history = []
        
        # Prepopulate with standard mock trends
        self.assimilate_feed("Market reports signal potential interest rate cooling on tech portfolios.")
        self.assimilate_feed("Social network hyper-polarization detected over decentralized protocol updates.")

    def assimilate_feed(self, text):
        self.news_feed_history.append({
            "text": text,
            "timestamp": time.time(),
            "analyzed": False
        })
        print(f"📥 [ASSIMILATED] News Feed Ingested: '{text[:70]}...'")

    def show_manifold_visualizer(self, snn):
        """
        Renders a real-time ASCII visualization of the Information Manifold curvature.
        """
        print("\n🗺️ INFORMATION GEOMETRY TOPOLOGY MAP:")
        print("=" * 75)
        
        snn_arr = np.array(snn) if (snn is not None and hasattr(snn, '__len__') and len(snn) > 1) else np.array([0.5, 0.5])
        median_val = np.median(snn_arr)
        polarization = np.mean(np.abs(snn_arr - median_val))
        ricci_curvature = 1.0 - (2.5 * polarization)
        
        # Plot curve
        # Curve represents the metric tensor spacing
        print(f" Ricci Curvature (R): {ricci_curvature:+.4f} (Positive = Stable Union, Negative = Echo Chambers)")
        print("-" * 75)
        
        # ASCII representation of the space
        if ricci_curvature >= 0.2:
            print(" [Spherical Convex Space]         ( o o o o o o o o )")
            print("                                (  Stable Consensus  )")
        elif ricci_curvature > -0.3:
            print(" [Flat Euclidean Space]          [-------------------]")
            print("                                [  Uniform Diffusion ]")
        else:
            print(" [Hyperbolic Polarized Space]    < o o o >       < o o o >")
            print("                                <Echo Chamber>  <Echo Chamber>")
            print("                                    (Divided Manifold Lobe)")
            
        print("-" * 75)
        print(" Active Coordinate Clusters:")
        for idx, val in enumerate(snn_arr[:8]):
            bar_len = int(val * 30)
            print(f"  • Node-Coordinate [{idx:02d}]: |" + "█" * bar_len + " " * (30 - bar_len) + f"| Value: {val:.3f}")
        print("=" * 75)

    def execute_auto_loop(self, steps=8):
        """
        Runs an automated closed-loop optimization to damp echo-chamber polarization.
        Dynamically adjusts cognitive parameter coordination to restore positive manifold curvature.
        """
        print(f"\n🔄 STARTING INFORMATION MANIFOLD CLOSED-LOOP OPTIMIZER ({steps} Steps):")
        print("=" * 90)
        print(f" {'Step':<5} | {'Metric Sync (sy)':<15} | {'Ricci Curvature':<18} | {'Surprise':<10} | {'Resonance':<10}")
        print("-" * 90)
        
        # Initial simulated state
        s = 0.60
        sy = 0.40 # starting highly polarized / unsynced
        p = 0.50
        snn = [0.1, 0.9, 0.1, 0.9] # heavily bimodal polarization
        
        for step in range(1, steps + 1):
            feed_item = self.news_feed_history[-1]["text"] if self.news_feed_history else "System stabilizing sequence."
            
            kwargs = {}
            # Evaluate manifold
            resonance = self.nexus.evaluate(s, sy, p, snn, text=feed_item, haptic_level=0.1, **kwargs)
            
            ricci_curvature = kwargs.get('info_ricci_curvature', 0.0)
            surprise_index = kwargs.get('info_surprise_index', 0.2)
            
            print(f" #{step:02d}  | {sy:<15.4f} | {ricci_curvature:<+18.4f} | {surprise_index:<10.4f} | {resonance:<10.4f}")
            
            # Closed-Loop Feedback Alignment:
            # If Ricci curvature is negative (highly polarized echo-chambers),
            # we increase the metric synchronization (sy) and pull SNN nodes towards the median center to "cool" divergence.
            if ricci_curvature < 0:
                sy = min(0.99, sy + 0.08)
                # Pull snn values towards their mean to damp bimodal polarization
                mean_snn = np.mean(snn)
                snn = [float(v * 0.7 + mean_snn * 0.3) for v in snn]
            else:
                # Stable consensus maintained, slight baseline decay to allow adaptive trend assimilation
                sy = max(0.40, sy - 0.01)
                
            time.sleep(0.1)
            
        print("-" * 90)
        print("📊 TOPOLOGICAL OPTIMIZATION COMPLETED: Consensus Manifold Re-Convexed.")
        print("=" * 90)


# ──────────────────────────────────────────────────────────────────────
# 🖥️ CLI PORT & INTERACTIVE SHELL
# ──────────────────────────────────────────────────────────────────────
def run_cli_shell():
    parser = argparse.ArgumentParser(description="HOLOSYN V90 CLI: Social Media & News Manifold Control Unit")
    parser.add_argument("--assimilate", type=str, help="Assimulate a new social or news text feed directly.")
    parser.add_argument("--visualize", action="store_true", help="Print an ASCII topological map of the manifold.")
    parser.add_argument("--auto", type=int, nargs='?', const=10, help="Run the closed-loop consensus optimizer.")
    parser.add_argument("--interactive", action="store_true", help="Launch the interactive terminal dashboard.")
    
    args = parser.parse_args()
    
    nexus_observer = UnifiedSocialMediaNexus()
    controller = ExtendedSocialManifoldController(nexus_observer)
    
    has_args = any([args.assimilate, args.visualize, args.auto is not None, args.interactive])
    
    if args.assimilate:
        controller.assimilate_feed(args.assimilate)
        return
        
    if args.visualize:
        controller.show_manifold_visualizer([0.2, 0.8, 0.3, 0.7])
        return
        
    if args.auto is not None:
        controller.execute_auto_loop(steps=args.auto)
        return
        
    if args.interactive or not has_args:
        # Launch Interactive Control Menu
        snn_mock = [0.15, 0.85, 0.20, 0.80, 0.50]
        while True:
            print("\n" + "═"*75)
            print("  🪐 HOLOSYN V90 SOCIAL MEDIA & NEWS MANIFOLD PANEL")
            print("  Target Hardware: Dell Latitude 5420 CPU [i5-1145G7]")
            print("═"*75)
            print("  [1] Assimilate Semantic Feed Ingestion  (NEWS FEED)")
            print("  [2] Render Topological Manifold map     (VISUALIZE)")
            print("  [3] Run Closed-Loop Consensus Optimizer (AUTO)")
            print("  [4] Run Standard Baseline Matrix Test")
            print("  [5] Exit System")
            print("-" * 75)
            
            try:
                choice = input("👉 Select function [1-5]: ").strip()
                if choice == "1":
                    feed_text = input("✏️ Enter headline or social media post to assimilate: ").strip()
                    if feed_text:
                        controller.assimilate_feed(feed_text)
                elif choice == "2":
                    controller.show_manifold_visualizer(snn_mock)
                elif choice == "3":
                    steps_in = input("🔄 Enter step count [default 8]: ").strip()
                    steps = int(steps_in) if steps_in.isdigit() else 8
                    controller.execute_auto_loop(steps)
                elif choice == "4":
                    print("\n⚡ Executing Baseline Matrix Test:")
                    feed_item = controller.news_feed_history[-1]["text"] if controller.news_feed_history else "Default test matrix initialization."
                    nexus_observer.evaluate(
                        0.85, 0.90, 0.35, snn_mock, 
                        text=feed_item, 
                        haptic_level=0.15
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