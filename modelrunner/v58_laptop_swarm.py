#!/usr/bin/env python3
"""
HOLOSYN V5.8: LAPTOP-OPTIMIZED AGENTIC SWARM
================================================================
Hardware Target: Intel i5-1145G7 (AVX-512), 16GB RAM (CPU-Only)
Strategy: Dynamic Model Swapping, bfloat16 Quantization, Strict GC.
"""

import os
import gc
import torch
import numpy as np
import time
import random
from PIL import Image

warnings = __import__('warnings')
warnings.filterwarnings("ignore")

try:
    from __main__ import BaseObserver
except ImportError:
    class BaseObserver:
        def evaluate(self, s, sy, p, snn, text="", haptic_level=0.0, **kwargs): return 0.5

try:
    from transformers import AutoTokenizer, AutoModelForCausalLM, Qwen2VLForConditionalGeneration, AutoProcessor, WhisperProcessor, WhisperForConditionalGeneration
    HF_AVAILABLE = True
except ImportError:
    HF_AVAILABLE = False
    print("❌ ERROR: pip install transformers accelerate torchvision")

# ---------------------------------------------------------
# 1. HARDWARE-LOCKED SWARM MANAGER
# ---------------------------------------------------------
class LaptopSwarmManager:
    """Singleton manager that strictly controls RAM allocation."""
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(LaptopSwarmManager, cls).__new__(cls)
            cls._instance.device = "cpu"
            # 11th Gen Intel CPUs support bfloat16, slashing RAM usage by 50%
            cls._instance.dtype = torch.bfloat16 
            
            cls._instance.active_model_name = None
            cls._instance.model = None
            cls._instance.processor = None
            cls._instance.tokenizer = None
        return cls._instance

    def flush_memory(self):
        """Aggressively clears RAM to prevent freezing."""
        if self.model is not None:
            print(f"   🧹 [SWARM MANAGER] Unloading {self.active_model_name} from RAM...")
            del self.model
            del self.processor
            del self.tokenizer
            self.model = None
            self.processor = None
            self.tokenizer = None
        gc.collect()

    def load_agent(self, model_name, is_vision=False, is_audio=False):
        """Loads a model ONLY if it isn't already in RAM."""
        if self.active_model_name == model_name:
            return True # Already active

        if not HF_AVAILABLE: return False

        self.flush_memory()
        print(f"   ⏳ [SWARM MANAGER] Allocating RAM for {model_name} (bfloat16)...")
        
        try:
            if is_vision:
                self.processor = AutoProcessor.from_pretrained(model_name)
                self.model = Qwen2VLForConditionalGeneration.from_pretrained(
                    model_name, torch_dtype=self.dtype
                ).to(self.device).eval()
            elif is_audio:
                self.processor = WhisperProcessor.from_pretrained(model_name)
                self.model = WhisperForConditionalGeneration.from_pretrained(
                    model_name, torch_dtype=self.dtype
                ).to(self.device).eval()
            else:
                self.tokenizer = AutoTokenizer.from_pretrained(model_name)
                if self.tokenizer.pad_token is None: self.tokenizer.pad_token = self.tokenizer.eos_token
                self.model = AutoModelForCausalLM.from_pretrained(
                    model_name, torch_dtype=self.dtype
                ).to(self.device).eval()
                
            self.active_model_name = model_name
            print("   ✅ [SWARM MANAGER] Agent locked into CPU Memory.")
            return True
        except Exception as e:
            print(f"   ❌ [SWARM MANAGER] Allocation Failed: {e}")
            self.flush_memory()
            return False

# ---------------------------------------------------------
# 2. THE AGENTIC OBSERVER
# ---------------------------------------------------------
class LaptopAgenticSwarmObserver(BaseObserver):
    def __init__(self):
        super().__init__()
        self.manager = LaptopSwarmManager()
        self.history = []
        
        # Start with the fast 0.5B reasoning agent
        self.manager.load_agent("Qwen/Qwen2.5-0.5B-Instruct")
        print("🧠 [AGENTIC SWARM] Active. Calibrated for 16GB i5-1145G7.")

    def evaluate(self, s, sy, p, snn, text="", haptic_level=0.0, **kwargs):
        self.history.append(s)
        if len(self.history) > 10: self.history.pop(0)

        modality = kwargs.get('mod', 'TEXT')
        file_path = kwargs.get('file_path', None)

        # --- DYNAMIC SWARM ROUTING LOGIC ---
        if modality == "IMAGE_NODE" or (file_path and file_path.endswith(('.png', '.jpg', '.jpeg'))):
            # Heavy Vision Agent (4.5GB RAM)
            self.manager.load_agent("Qwen/Qwen2-VL-2B-Instruct", is_vision=True)
            
        elif modality == "AUDIO_NODE":
            # Audio Transcription Agent
            self.manager.load_agent("openai/whisper-tiny", is_audio=True)
            
        elif np.mean(self.history) < 0.25:
            # Cognitive Crisis: Fall back to ultra-light model to process without freezing
            print("   ⚠️ [AGENTIC SWARM] System Crisis Detected. Routing to OPT-125m for stability.")
            self.manager.load_agent("facebook/opt-125m")
            kwargs['gain_multiplier'] = 0.5
            
        elif self.manager.active_model_name not in ["Qwen/Qwen2.5-0.5B-Instruct", "Qwen/Qwen2-VL-2B-Instruct"]:
            # Default to the highly capable 0.5B reasoning model
            self.manager.load_agent("Qwen/Qwen2.5-0.5B-Instruct")

        # --- SUBCONSCIOUS GENERATION (Hooking into evaluate loop) ---
        # Instead of replacing the generator, the observer handles the generation 
        # and stores it in kwargs for the UI to print.
        
        if self.manager.model:
            context = f"System Phase: {p:.2f}. Coh: {s:.2f}. "
            try:
                if "Qwen2-VL" in self.manager.active_model_name and file_path:
                    img = Image.open(file_path).convert("RGB")
                    msgs = [{"role": "user", "content": [{"type": "image", "image": img}, {"type": "text", "text": "Analyze Holosyn resonance of this image in 10 words."}]}]
                    prompt = self.manager.processor.apply_chat_template(msgs, tokenize=False, add_generation_prompt=True)
                    inputs = self.manager.processor(text=[prompt], images=[img], return_tensors="pt").to(self.manager.device)
                    with torch.no_grad():
                        out = self.manager.model.generate(**inputs, max_new_tokens=15)
                    kwargs['swarm_hallucination'] = self.manager.processor.batch_decode(out, skip_special_tokens=True)[0].strip()
                    
                elif "opt" in self.manager.active_model_name or "Qwen2.5" in self.manager.active_model_name:
                    inputs = self.manager.tokenizer(context + "The system concludes:", return_tensors="pt").to(self.manager.device)
                    with torch.no_grad():
                        out = self.manager.model.generate(**inputs, max_new_tokens=10, do_sample=True, temperature=0.7)
                    kwargs['swarm_hallucination'] = self.manager.tokenizer.decode(out[0][inputs.input_ids.size(1):], skip_special_tokens=True).strip()
            except Exception as e:
                pass # Prevent loop crash

        return float(np.clip((s * 0.5) + (p * 0.5), 0.0, 1.0))