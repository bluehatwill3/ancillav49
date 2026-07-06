#!/usr/bin/env python3
"""
HOLOSYN V76: MASTER COMPUTER VISION & SPATIAL DYNAMICS NEXUS (ARRAY-SAFE)
===================================================================================
Hardware Target: Dell Latitude 5420 (i5-1145G7 | 16GB RAM | CPU-Only)
Role: Models Spatial Entropy, Optical Flow, and Vision-Language Feature Extraction.
Integration: Deploys Moondream2 and native hive_img_only/hive_vid_only tensors.
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
from PIL import Image

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
            print(f"   🧬 [VISION CORE] Master structural weights mapped from: {os.path.basename(path)}")
            return True
        except Exception: return False


# ──────────────────────────────────────────────────────────────────────
# 👁️ NATIVE VISION ENCODER (hive_img_only.pt / hive_vid_only.pt)
# ──────────────────────────────────────────────────────────────────────
class NativeVisionWeightEncoder:
    """
    Ingests local visual tensors to extract latent spatial bounds directly.
    """
    def __init__(self):
        self.device = "cpu"
        self.img_weights = None
        self.vid_weights = None
        self._boot_visual_tensors()

    def _boot_visual_tensors(self):
        target_dir = "/home/devcbloom/Documents/Intellibloomenv/lang"
        img_paths = ["hive_img_only.pt", os.path.join(target_dir, "hive_img_only.pt"), "/home/devcbloom/Downloads/hive_img_only.pt"]
        vid_paths = ["hive_vid_only.pt", os.path.join(target_dir, "hive_vid_only.pt"), "/home/devcbloom/Downloads/hive_vid_only.pt"]
        
        for p in img_paths:
            if os.path.exists(p):
                try:
                    self.img_weights = torch.load(p, map_location=self.device, weights_only=False)
                    print(f"   ⚡ [NATIVE VISION] Bound localized image matrix: {os.path.basename(p)}")
                    break
                except Exception: pass
                
        for p in vid_paths:
            if os.path.exists(p):
                try:
                    self.vid_weights = torch.load(p, map_location=self.device, weights_only=False)
                    print(f"   ⚡ [NATIVE VISION] Bound localized video matrix: {os.path.basename(p)}")
                    break
                except Exception: pass

    def extract_visual_norm(self, snn_array, is_video=False):
        # Array-safe check
        snn_safe = np.array(snn_array) if (snn_array is not None and hasattr(snn_array, '__len__') and len(snn_array) > 0) else np.array([0.5, 0.5])
        
        active_weights = self.vid_weights if is_video else self.img_weights
        if not active_weights:
            return float(np.mean(snn_safe))
            
        try:
            # We treat the weight dict keys as dynamic filters. We calculate the Frobenius
            # norm of the dot product between the sensory array and the first dense weight layer.
            # This proxies how intensely the visual network "activates" on the current state.
            first_layer_key = list(active_weights.keys())[0]
            w_tensor = active_weights[first_layer_key]
            
            # Sub-sample or pad to match the dimensionality for a rough projection
            dim = w_tensor.shape[-1] if len(w_tensor.shape) > 0 else 1
            padded_snn = np.pad(snn_safe, (0, max(0, dim - len(snn_safe))), 'constant')[:dim]
            
            snn_tensor = torch.tensor(padded_snn, dtype=torch.float32)
            projection = torch.matmul(w_tensor.float(), snn_tensor)
            
            normalized_activation = torch.linalg.vector_norm(projection).item()
            return float(np.clip(normalized_activation / 100.0, 0.0, 1.0))
        except Exception:
            return float(np.mean(snn_safe))


# ──────────────────────────────────────────────────────────────────────
# 🖼️ HUGGINGFACE VISION-LANGUAGE SWARM
# ──────────────────────────────────────────────────────────────────────
try:
    from transformers import AutoModelForCausalLM, AutoTokenizer
    HF_AVAILABLE = True
except ImportError:
    HF_AVAILABLE = False

class VisionSymbolicMicroSwarm:
    def __init__(self):
        self.device = "cpu"
        self.dtype = torch.bfloat16
        self.model = None
        self.tokenizer = None
        self.active = False
        self._boot_model()

    def _boot_model(self):
        if not HF_AVAILABLE: return
        
        # We attempt to load moondream2 as it is optimized for rapid CPU edge inference
        model_id = "vikhyatk/moondream2"
        try:
            print(f"   ⏳ [VISION MICROMODEL] Allocating {model_id} to CPU...")
            self.model = AutoModelForCausalLM.from_pretrained(model_id, trust_remote_code=True, torch_dtype=self.dtype).eval()
            
            # Resolve the tracking bug patched in v58
            if not hasattr(self.model, 'all_tied_weights_keys'):
                self.model.all_tied_weights_keys = []
                
            self.tokenizer = AutoTokenizer.from_pretrained(model_id)
            self.active = True
            print("   ✅ [VISION MICROMODEL] Spatial/Image Reasoning Engine Locked.")
        except Exception as e: 
            print(f"   ⚠️ [VISION MICROMODEL] Visual model bypass active (Falling back to numerical CV).")

    def evaluate_symbolic_vision(self, spatial_entropy, file_path=None):
        if not self.active:
            return float(np.clip(1.0 - spatial_entropy, 0.0, 1.0))
            
        try:
            # If an actual image file is provided, process it
            if file_path and isinstance(file_path, str) and os.path.exists(file_path):
                img = Image.open(file_path).convert("RGB")
                enc_image = self.model.encode_image(img)
                response = self.model.answer_question(enc_image, "Is this image chaotic, blurry, or unstable? Answer only with a single float between 0.0 (Chaotic) and 1.0 (Stable).", self.tokenizer)
                match = re.search(r"0\.\d+|1\.0", response)
                if match: return float(match.group())
            
            # Fallback to abstract math interpretation
            return float(np.clip(1.0 - spatial_entropy, 0.0, 1.0))
        except Exception: 
            return 0.5


# ──────────────────────────────────────────────────────────────────────
# 📷 NUMERICAL COMPUTER VISION ENGINE
# ──────────────────────────────────────────────────────────────────────
class NumericalComputerVisionObserver(BaseObserver):
    """
    Computes image gradients, spatial entropy, and temporal optical flow proxies.
    """
    def __init__(self, hive_core=None):
        super().__init__()
        self.hive_core = hive_core if hive_core is not None else HiveFusionCore().eval()
        self.previous_snn_frame = None

    def calculate_spatial_entropy(self, snn):
        """
        Calculates Laplacian variance (sharpness proxy) and spatial entropy.
        """
        snn_arr = np.array(snn) if (snn is not None and hasattr(snn, '__len__') and len(snn) > 1) else np.array([0.5, 0.5])
        
        # Second derivative (Laplacian proxy)
        laplacian = np.diff(snn_arr, n=2) if len(snn_arr) > 2 else np.array([0.0])
        sharpness_variance = np.var(laplacian)
        
        # Shannon Entropy on spatial distribution
        p = np.abs(snn_arr) / (np.sum(np.abs(snn_arr)) + 1e-9)
        p = p[p > 0]
        spatial_entropy = -np.sum(p * np.log2(p + 1e-9))
        
        # High entropy & high variance means dense/noisy visual data
        normalized_entropy = np.clip(spatial_entropy / 4.0, 0.0, 1.0)
        return float(normalized_entropy), float(np.clip(sharpness_variance, 0.0, 1.0))

    def calculate_temporal_flow(self, snn):
        """
        Proxies optical flow by measuring the Euclidean distance between the current
        and previous execution frames.
        """
        snn_arr = np.array(snn) if (snn is not None and hasattr(snn, '__len__') and len(snn) > 0) else np.array([0.5])
        
        if self.previous_snn_frame is None or len(self.previous_snn_frame) != len(snn_arr):
            self.previous_snn_frame = snn_arr
            return 0.0
            
        # Euclidean displacement
        flow_magnitude = np.linalg.norm(snn_arr - self.previous_snn_frame)
        self.previous_snn_frame = snn_arr
        
        # Normalize motion vector (high flow = high frame delta/instability)
        return float(np.clip(flow_magnitude / np.sqrt(len(snn_arr)), 0.0, 1.0))


# ──────────────────────────────────────────────────────────────────────
# 🌐 MASTER VISION NEXUS ORCHESTRATOR
# ──────────────────────────────────────────────────────────────────────
class UnifiedVisionNexus(BaseObserver):
    def __init__(self):
        super().__init__()
        print("💠 [VISION NEXUS] Initializing Spatial CV Dynamics & Native Tensors...")
        
        self.hive_core = HiveFusionCore().eval()
        self._bind_master_weights()
        
        self.native_encoder = NativeVisionWeightEncoder()
        self.numerical_engine = NumericalComputerVisionObserver(self.hive_core)
        self.symbolic_engine = VisionSymbolicMicroSwarm()

    def _bind_master_weights(self):
        locations = ["hive_fused_all.pt", "hive_best.pt", "/home/devcbloom/Downloads/hive_fused_all.pt"]
        for path in locations:
            if self.hive_core.assimilate_hive(path):
                break

    def evaluate(self, s, sy, p, snn, text="", haptic_level=0.0, **kwargs):
        modality = kwargs.get('mod', 'TEXT')
        file_path = kwargs.get('file_path', None)
        is_video = (modality == 'VIDEO')
        
        # 1. Evaluate Numerical Computer Vision constraints
        spatial_entropy, sharpness = self.numerical_engine.calculate_spatial_entropy(snn)
        temporal_flow = self.numerical_engine.calculate_temporal_flow(snn)
        
        # 2. Extract Native Structural Yield via hive_img_only / hive_vid_only
        native_visual_yield = self.native_encoder.extract_visual_norm(snn, is_video)
        
        # 3. Evaluate Symbolic Vision using HuggingFace Micro-Model
        symbolic_vision_yield = self.symbolic_engine.evaluate_symbolic_vision(spatial_entropy, file_path)
        
        # Record into framework pipeline
        kwargs['vis_spatial_entropy'] = spatial_entropy
        kwargs['vis_temporal_flow'] = temporal_flow
        kwargs['vis_native_yield'] = native_visual_yield
        kwargs['vis_symbolic_yield'] = symbolic_vision_yield
        
        print(f"   👁️ [COMPUTER VISION] Entropy: {spatial_entropy:.3f} | Motion Flow: {temporal_flow:.3f} | Sharpness: {sharpness:.3f}")
        print(f"   ⚡ [NATIVE PT YIELD]: {native_visual_yield:.4f} | 🤖 [SYMBOLIC YIELD]: {symbolic_vision_yield:.4f}")

        try:
            snn_density = float(np.mean(snn)) if (snn is not None and hasattr(snn, '__len__') and len(snn) > 0) else 0.5
            
            # Vector allocation: [Coherence, Spatial Entropy, Flow Stability, Native Extraction Yield, Symbolic Yield]
            flow_stability = 1.0 - temporal_flow
            state_matrix = torch.tensor([[[s, spatial_entropy, flow_stability, native_visual_yield, symbolic_vision_yield]]], dtype=torch.float32)
            
            with torch.no_grad():
                master_judgment = self.hive_core(state_matrix).item()
        except Exception:
            master_judgment = 0.5

        # Compile final unified vision resonance
        final_resonance = np.clip((native_visual_yield * 0.3) + (symbolic_vision_yield * 0.3) + (master_judgment * 0.4), 0.0, 1.0)
        
        print(f"📊 [VISION NEXUS TOTAL RESONANCE]: {final_resonance:.4f}")
        print("═" * 80)
        return float(final_resonance)


# Register global variables for strict validation scanner checks
observer = UnifiedVisionNexus()
plugin_observer = observer

if __name__ == "__main__":
    # Baseline framework execution verification
    observer.evaluate(0.85, 0.90, 0.50, [0.4, 0.5, 0.45, 0.55], text="Visual validation.", haptic_level=0.1, mod='IMAGE')