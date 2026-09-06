#!/usr/bin/env python3
"""
HOLOSYN V79: MASTER NETWORK TOPOLOGY & GRAPH THEORY NEXUS (ARRAY-SAFE)
===================================================================================
Hardware Target: Dell Latitude 5420 (i5-1145G7 | 16GB RAM | CPU-Only)
Role: Models Graph Laplacian, Algebraic Connectivity, and Physical Bandwidth.
Integration: Fuses psutil network I/O with Qwen 0.5B Symbolic Topology Logic.
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
            print(f"   🧬 [NETWORK CORE] Topology weights mapped from: {os.path.basename(path)}")
            return True
        except Exception: return False


# ──────────────────────────────────────────────────────────────────────
# 📡 PHYSICAL NETWORK I/O SCANNER
# ──────────────────────────────────────────────────────────────────────
class PhysicalNetworkScanner:
    """
    Queries real-time network interfaces (Wi-Fi/Ethernet) via psutil.
    Calculates bandwidth saturation and simulated packet drop ratios.
    """
    def __init__(self):
        self.psutil_active = PSUTIL_AVAILABLE
        self.last_bytes_sent = 0
        self.last_bytes_recv = 0
        self.last_time = time.time()
        
        # Max theoretical sustained Wi-Fi 6 bandwidth proxy (e.g., ~50 MB/s)
        self.max_bandwidth_bps = 50 * 1024 * 1024 
        
        if self.psutil_active:
            try:
                io = psutil.net_io_counters()
                self.last_bytes_sent = io.bytes_sent
                self.last_bytes_recv = io.bytes_recv
            except Exception:
                self.psutil_active = False

    def fetch_bandwidth_saturation(self, haptic_level):
        current_time = time.time()
        dt = max(current_time - self.last_time, 0.001)
        
        if self.psutil_active:
            try:
                io = psutil.net_io_counters()
                sent_delta = io.bytes_sent - self.last_bytes_sent
                recv_delta = io.bytes_recv - self.last_bytes_recv
                
                self.last_bytes_sent = io.bytes_sent
                self.last_bytes_recv = io.bytes_recv
                self.last_time = current_time
                
                total_bps = (sent_delta + recv_delta) / dt
                saturation = np.clip(total_bps / self.max_bandwidth_bps, 0.0, 1.0)
            except Exception:
                saturation = haptic_level * 0.5
        else:
            # Fallback heuristic: Hardware friction induces virtual network congestion
            saturation = np.clip(haptic_level * 0.8, 0.0, 1.0)
            
        # Simulated Packet Loss (spikes when system is choked)
        packet_loss_proxy = np.clip(saturation * haptic_level, 0.0, 1.0)
        
        return float(saturation), float(packet_loss_proxy)


# ──────────────────────────────────────────────────────────────────────
# 🕸️ ABSTRACT GRAPH THEORY & TOPOLOGY ENGINE
# ──────────────────────────────────────────────────────────────────────
class GraphTheoryObserver(BaseObserver):
    """
    Treats the cognitive SNN arrays as network nodes. Calculates Adjacency Matrices,
    Graph Density, and Algebraic Connectivity (Fiedler value) to ensure the swarm
    is not mathematically fracturing.
    """
    def __init__(self, hive_core=None):
        super().__init__()
        self.hive_core = hive_core if hive_core is not None else HiveFusionCore().eval()

    def evaluate_graph_topology(self, snn):
        # 🛠️ Array-safe sanitization
        if snn is None or not hasattr(snn, '__len__') or len(snn) < 2:
            snn_arr = np.array([0.5, 0.6, 0.4])
        else:
            snn_arr = np.array(snn)
            
        # Ensure we have a reasonable size limit for CPU matrix math (max 16x16)
        if len(snn_arr) > 16:
            snn_arr = snn_arr[:16]

        n_nodes = len(snn_arr)
        
        try:
            # 1. Adjacency Matrix (A): Outer product of SNN states representing connection strength
            A = np.outer(snn_arr, snn_arr)
            # Remove self-loops (diagonal = 0)
            np.fill_diagonal(A, 0.0)
            
            # Graph Density: Ratio of current edge weights to maximum possible connections
            max_edges = n_nodes * (n_nodes - 1)
            density = np.sum(A) / max_edges if max_edges > 0 else 0.5
            density = float(np.clip(density, 0.0, 1.0))

            # 2. Degree Matrix (D): Diagonal matrix of node connection sums
            degrees = np.sum(A, axis=1)
            D = np.diag(degrees)
            
            # 3. Graph Laplacian (L = D - A)
            L = D - A
            
            # 4. Algebraic Connectivity (Fiedler Value)
            # The second smallest eigenvalue of the Laplacian matrix.
            # If > 0, the graph is connected. If ~0, the network is disconnected/fractured.
            eigenvalues = np.real(np.linalg.eigvals(L))
            sorted_eigenvals = np.sort(eigenvalues)
            
            if len(sorted_eigenvals) >= 2:
                algebraic_connectivity = sorted_eigenvals[1]
            else:
                algebraic_connectivity = 0.0
                
            # Normalize the connectivity based on node count to get a 0.0 - 1.0 stability index
            connectivity_index = np.clip(algebraic_connectivity / (n_nodes + 1e-5), 0.0, 1.0)
            
            return density, float(connectivity_index)
            
        except Exception as e:
            # Fallback if matrix decomposition fails
            return 0.5, 0.5


# ──────────────────────────────────────────────────────────────────────
# 🧠 HUGGINGFACE SYMBOLIC ROUTING SWARM
# ──────────────────────────────────────────────────────────────────────
try:
    from transformers import AutoModelForCausalLM, AutoTokenizer
    HF_AVAILABLE = True
except ImportError:
    HF_AVAILABLE = False

class TopologySymbolicMicroSwarm:
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
            print(f"   ⏳ [TOPOLOGY MICROMODEL] Allocating {model_id} to CPU...")
            self.model = AutoModelForCausalLM.from_pretrained(model_id, torch_dtype=self.dtype).eval()
            self.tokenizer = AutoTokenizer.from_pretrained(model_id)
            self.active = True
            print("   ✅ [TOPOLOGY MICROMODEL] Symbolic Routing Engine Locked.")
        except Exception as e: 
            print(f"   ⚠️ [TOPOLOGY MICROMODEL] Model bypass active. {e}")

    def evaluate_routing_stability(self, connectivity, bw_saturation):
        if not self.active:
            return float(np.clip(connectivity - (bw_saturation * 0.5), 0.0, 1.0))
            
        prompt = f"Graph Algebraic Connectivity = {connectivity:.3f}. Network Bandwidth Saturation = {bw_saturation*100:.1f}%. Is the routing topology robust and uncongested? Output only a float between 0.0 (Disconnected/Congested) and 1.0 (Robust)."
        try:
            inputs = self.tokenizer(prompt, return_tensors="pt")
            with torch.no_grad():
                outputs = self.model.generate(**inputs, max_new_tokens=10, do_sample=False)
            response = self.tokenizer.decode(outputs[0][inputs.input_ids.size(1):], skip_special_tokens=True)
            match = re.search(r"0\.\d+|1\.0", response)
            if match: return float(match.group())
            return float(np.clip(connectivity, 0.0, 1.0))
        except Exception: 
            return 0.5


# ──────────────────────────────────────────────────────────────────────
# 🌐 MASTER NETWORKS NEXUS ORCHESTRATOR
# ──────────────────────────────────────────────────────────────────────
class UnifiedNetworksNexus(BaseObserver):
    def __init__(self):
        super().__init__()
        print("💠 [NETWORKS NEXUS] Initializing Graph Theory & Topology Matrices...")
        
        self.hive_core = HiveFusionCore().eval()
        self._bind_master_weights()
        
        self.io_scanner = PhysicalNetworkScanner()
        self.graph_engine = GraphTheoryObserver(self.hive_core)
        self.symbolic_engine = TopologySymbolicMicroSwarm()

    def _bind_master_weights(self):
        locations = ["hive_fused_all.pt", "hive_best.pt", "/home/devcbloom/Downloads/hive_fused_all.pt"]
        for path in locations:
            if self.hive_core.assimilate_hive(path):
                break

    def evaluate(self, s, sy, p, snn, text="", haptic_level=0.0, **kwargs):
        
        # 1. Evaluate Abstract Graph Topology
        graph_density, algebraic_connectivity = self.graph_engine.evaluate_graph_topology(snn)
        
        # 2. Evaluate Physical Network I/O Saturation
        bw_saturation, packet_loss = self.io_scanner.fetch_bandwidth_saturation(haptic_level)
        
        # 3. Evaluate Symbolic Routing Health
        symbolic_routing_yield = self.symbolic_engine.evaluate_routing_stability(algebraic_connectivity, bw_saturation)
        
        # Record variables for global scope access
        kwargs['net_graph_density'] = graph_density
        kwargs['net_algebraic_conn'] = algebraic_connectivity
        kwargs['net_bw_saturation'] = bw_saturation
        kwargs['net_packet_loss'] = packet_loss
        
        print(f"   🕸️ [GRAPH TOPOLOGY] Density: {graph_density:.3f} | Alg. Connectivity (Fiedler): {algebraic_connectivity:.3f}")
        print(f"   📡 [PHYSICAL I/O] BW Saturation: {bw_saturation*100:.1f}% | Packet Loss Proxy: {packet_loss*100:.1f}%")
        print(f"   🤖 [SYMBOLIC ROUTING YIELD]: {symbolic_routing_yield:.4f}")

        try:
            snn_density = float(np.mean(snn)) if (snn is not None and hasattr(snn, '__len__') and len(snn) > 0) else 0.5
            
            # Vector allocation mapping: [Connectivity, Inverse Saturation, Inverse Packet Loss, SNN Density, Symbolic Yield]
            state_matrix = torch.tensor([[[algebraic_connectivity, (1.0 - bw_saturation), (1.0 - packet_loss), snn_density, symbolic_routing_yield]]], dtype=torch.float32)
            
            with torch.no_grad():
                master_judgment = self.hive_core(state_matrix).item()
        except Exception:
            master_judgment = 0.5

        # Compile final unified network resonance
        final_resonance = np.clip((algebraic_connectivity * 0.3) + (symbolic_routing_yield * 0.3) + (master_judgment * 0.4), 0.0, 1.0)
        
        # Penalty for extreme network congestion or packet loss
        throttle_factor = np.clip(1.0 - (packet_loss * 0.5), 0.1, 1.0)
        final_resonance = final_resonance * throttle_factor
        
        print(f"📊 [NETWORKS NEXUS TOTAL RESONANCE]: {final_resonance:.4f}")
        print("═" * 80)
        return float(final_resonance)


# Register global variables for strict validation scanner checks
observer = UnifiedNetworksNexus()
plugin_observer = observer

if __name__ == "__main__":
    # Baseline framework execution verification
    mock_payload = "Evaluating graph Laplacian and network bandwidth layers."
    observer.evaluate(0.85, 0.90, 0.50, [0.4, 0.8, 0.6, 0.5], text=mock_payload, haptic_level=0.1)