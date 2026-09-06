#!/usr/bin/env python3
"""
HOLOSYN V5.8: ULTRA-SWARM FUSION NEXUS
===================================================================
Hardware: Dell Latitude 5420 (i5-1145G7 | 16GB RAM | CPU-Only)
Architecture: Central 'HiveFusionCore' orchestrated by dynamic Micro-Models.
"""

import os
import gc
import torch
import torch.nn as nn
import numpy as np
import warnings
from PIL import Image

warnings.filterwarnings("ignore")

try:
    from __main__ import BaseObserver
except ImportError:
    class BaseObserver:
        def evaluate(self, s, sy, p, snn, text="", haptic_level=0.0, **kwargs): return 0.5

try:
    from transformers import (
        AutoTokenizer, AutoModelForCausalLM, AutoProcessor,
        Qwen2VLForConditionalGeneration, WhisperProcessor, 
        WhisperForConditionalGeneration, AutoModel
    )
    HF_AVAILABLE = True
except ImportError:
    HF_AVAILABLE = False


# ──────────────────────────────────────────────────────────────────────
# 1. THE CENTRAL INTEGRATOR (hive_fused_all / hive_best)
# ──────────────────────────────────────────────────────────────────────
class HiveFusionCore(nn.Module):
    """
    The master structure designed to load `hive_fused_all.pt` or `hive_best.pt`.
    All micro-models send their semantic output here for final resonance scoring.
    """
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
        if x.dim() < 2 or x.size(1) == 0: return torch.tensor([0.0])
        seq_len = min(x.size(1), 512)
        emb = self.embedding(x[:, :seq_len, :]) + self.pos_encoder[:, :seq_len, :]
        return torch.tanh(self.projector(self.transformer(emb).mean(dim=1)).squeeze(-1))

    def assimilate_hive(self, path):
        if not os.path.exists(path): return False
        try:
            # Force map to CPU for Dell Latitude compatibility
            weights = torch.load(path, map_location="cpu", weights_only=False)
            if hasattr(weights, 'state_dict'): weights = weights.state_dict()
            
            # Clean keys to match standard TransformerCore topology
            import re
            clean_dict = {re.sub(r'^(enc\.|text\.|net\.|0\.|module\.)', '', k): v for k, v in weights.items() if isinstance(v, torch.Tensor)}
            self.load_state_dict(clean_dict, strict=False)
            print(f"   🧬 [HIVE FUSION] Successfully integrated master weights from: {os.path.basename(path)}")
            return True
        except Exception as e:
            print(f"   ⚠️ [HIVE FUSION] Topology mismatch during assimilation: {e}")
            return False


# ──────────────────────────────────────────────────────────────────────
# 2. MICRO-MODEL SWARM MANAGER (RAM Guardian)
# ──────────────────────────────────────────────────────────────────────
class UltraSwarmManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(UltraSwarmManager, cls).__new__(cls)
            cls._instance.device = "cpu"
            cls._instance.dtype = torch.bfloat16 # AVX-512 optimization
            
            cls._instance.active_model = None
            cls._instance.model = None
            cls._instance.processor = None
            
            # The comprehensive micro-model whitelist for 16GB laptops
            cls._instance.whitelist = {
                "vision_fast": "vikhyatk/moondream2",
                "vision_deep": "Qwen/Qwen2-VL-2B-Instruct",
                "audio": "openai/whisper-tiny",
                "text_logic": "Qwen/Qwen2.5-0.5B-Instruct",
                "text_causal": "TinyLlama/TinyLlama-1.1B-Chat-v1.0",
                "text_crisis": "HuggingFaceTB/SmolLM-135M-Instruct",
                "semantic": "sentence-transformers/all-MiniLM-L6-v2"
            }
        return cls._instance

    def purge(self):
        if self.model is not None:
            print(f"   🧹 [SWARM] Unloading {self.active_model}...")
            del self.model
            del self.processor
            self.model = None
            self.processor = None
            self.active_model = None
        gc.collect()

    def route_modality(self, role):
        target = self.whitelist.get(role)
        if not target or self.active_model == target: return True
        
        self.purge()
        print(f"   ⏳ [SWARM] Booting Micro-Model: {target} (bfloat16)...")
        
        try:
            if "moondream" in target:
                from transformers import AutoModelForCausalLM
                self.model = AutoModelForCausalLM.from_pretrained(target, trust_remote_code=True, torch_dtype=self.dtype).eval()
                self.processor = AutoTokenizer.from_pretrained(target)
            elif "VL" in target:
                self.processor = AutoProcessor.from_pretrained(target)
                self.model = Qwen2VLForConditionalGeneration.from_pretrained(target, torch_dtype=self.dtype).eval()
            elif "whisper" in target:
                self.processor = WhisperProcessor.from_pretrained(target)
                self.model = WhisperForConditionalGeneration.from_pretrained(target, torch_dtype=self.dtype).eval()
            else:
                self.processor = AutoTokenizer.from_pretrained(target)
                if self.processor.pad_token is None: self.processor.pad_token = self.processor.eos_token
                self.model = AutoModelForCausalLM.from_pretrained(target, torch_dtype=self.dtype).eval()
                
            self.active_model = target
            print("   ✅ [SWARM] Hardware Lock Confirmed.")
            return True
        except Exception as e:
            print(f"   ❌ [SWARM] Boot Failed: {e}")
            self.purge()
            return False


# ──────────────────────────────────────────────────────────────────────
# 3. THE OMNI-MODALITY OBSERVER
# ──────────────────────────────────────────────────────────────────────
class UltraSwarmObserver(BaseObserver):
    def __init__(self):
        super().__init__()
        self.swarm = UltraSwarmManager()
        self.hive_core = HiveFusionCore().eval()
        
        # Load the central integrated weights uploaded by the user
        print("🧠 [ULTRA-SWARM] Initializing Central Hive Fusion Core...")
        
        # Attempt to load the fused files from local directories
        paths_to_try = [
            "/home/devcbloom/Downloads/hive_fused_all.pt",
            "/home/devcbloom/Downloads/hive_best.pt",
            "hive_fused_all.pt", 
            "hive_best.pt"
        ]
        
        for path in paths_to_try:
            if self.hive_core.assimilate_hive(path):
                break

    def evaluate(self, s, sy, p, snn, text="", haptic_level=0.0, **kwargs):
        mod = kwargs.get('mod', 'TEXT')
        file_path = kwargs.get('file_path', None)
        
        hallucinated_text = text

        # 1. DYNAMIC MICRO-MODEL ROUTING
        if mod == "IMAGE_NODE" or (file_path and file_path.lower().endswith(('.png', '.jpg', '.jpeg'))):
            # Use Moondream2 for fast laptop vision instead of Qwen to save RAM
            if self.swarm.route_modality("vision_fast") and self.swarm.model:
                try:
                    img = Image.open(file_path).convert("RGB")
                    enc_image = self.swarm.model.encode_image(img)
                    hallucinated_text = self.swarm.model.answer_question(enc_image, "Describe the visual resonance of this image concisely.", self.swarm.processor)
                    kwargs['swarm_hallucination'] = f"[MOONDREAM SIGHT]: {hallucinated_text}"
                except Exception as e:
                    pass
                    
        elif mod == "AUDIO_NODE":
            if self.swarm.route_modality("audio"):
                pass # Handled upstream by Whisper, but we lock the model here just in case
                
        else:
            # TEXT LOGIC ROUTING
            if s < 0.3:
                # System in crisis / lagging: use ultra-fast SmolLM
                self.swarm.route_modality("text_crisis")
            else:
                # System stable: use Qwen 0.5B for deep reasoning
                self.swarm.route_modality("text_logic")
                
            if self.swarm.model and hasattr(self.swarm, 'processor'):
                try:
                    inputs = self.swarm.processor(f"Observe: {text}. The swarm concludes:", return_tensors="pt")
                    with torch.no_grad():
                        out = self.swarm.model.generate(**inputs, max_new_tokens=20)
                    hallucinated_text = self.swarm.processor.decode(out[0], skip_special_tokens=True).strip()
                    kwargs['swarm_hallucination'] = f"[SWARM LOGIC]: {hallucinated_text}"
                except: pass

        # 2. INTEGRATION THROUGH THE CENTRAL HIVE CORE
        # Map the resulting state into a 5D tensor for the hive_fused_all.pt core
        try:
            entropy = len(hallucinated_text) / 200.0 if hallucinated_text else 0.5
            state_vector = torch.tensor([[[s, sy, p, np.mean(snn) if len(snn) else 0.5, entropy]]], dtype=torch.float32)
            
            with torch.no_grad():
                # The Hive Core judges the output of the micro-models
                hive_judgment = self.hive_core(state_vector).item()
        except:
            hive_judgment = 0.5

        # Final Resonance combines Swarm coherence with Master Hive Judgment
        final_score = np.clip((s * 0.4) + (hive_judgment * 0.6), 0.0, 1.0)
        return float(final_score)


if __name__ == "__main__":
    print("💠 INITIATING ULTRA-SWARM FUSION TEST 💠")
    obs = UltraSwarmObserver()
    res = obs.evaluate(0.8, 0.8, 0.5, [0.5], text="Initiate swarm protocol.", mod="TEXT")
    print(f"Test Resonance: {res:.4f}")