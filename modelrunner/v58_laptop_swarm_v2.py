#!/usr/bin/env python3
"""
HOLOSYN V5.8: SELF-REFLECTIVE AGENTIC SWARM
================================================================
Hardware Target: Intel i5-1145G7, 16GB RAM (CPU-Only)
Upgrades: LLM JSON-Parsing for Auto-Tuning Gain, Entropy, and Model State.
"""

import os
import gc
import json
import re
import torch
import numpy as np
import time
import warnings
from PIL import Image

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

# ---------------------------------------------------------
# 1. HARDWARE-LOCKED SWARM MANAGER
# ---------------------------------------------------------
class LaptopSwarmManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(LaptopSwarmManager, cls).__new__(cls)
            cls._instance.device = "cpu"
            cls._instance.dtype = torch.bfloat16 # Crucial for 11th Gen i5
            
            cls._instance.active_model_name = None
            cls._instance.model = None
            cls._instance.processor = None
            cls._instance.tokenizer = None
            
            # HARDWARE WHITELIST: Prevent LLM from requesting models that cause OOM
            cls._instance.allowed_models = [
                "facebook/opt-125m",
                "Qwen/Qwen2.5-0.5B-Instruct",
                "Qwen/Qwen2-VL-2B-Instruct",
                "openai/whisper-tiny"
            ]
        return cls._instance

    def flush_memory(self):
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
        if self.active_model_name == model_name: return True
        if not HF_AVAILABLE: return False
        if model_name not in self.allowed_models:
            print(f"   🛡️ [SWARM GUARD] Blocked LLM request to load unverified model: {model_name}")
            return False

        self.flush_memory()
        print(f"   ⏳ [SWARM MANAGER] Allocating RAM for {model_name} (bfloat16)...")
        
        try:
            if is_vision:
                self.processor = AutoProcessor.from_pretrained(model_name)
                self.model = Qwen2VLForConditionalGeneration.from_pretrained(model_name, torch_dtype=self.dtype).eval()
            elif is_audio:
                self.processor = WhisperProcessor.from_pretrained(model_name)
                self.model = WhisperForConditionalGeneration.from_pretrained(model_name, torch_dtype=self.dtype).eval()
            else:
                self.tokenizer = AutoTokenizer.from_pretrained(model_name)
                if self.tokenizer.pad_token is None: self.tokenizer.pad_token = self.tokenizer.eos_token
                self.model = AutoModelForCausalLM.from_pretrained(model_name, torch_dtype=self.dtype).eval()
                
            self.active_model_name = model_name
            print("   ✅ [SWARM MANAGER] Agent locked into CPU Memory.")
            return True
        except Exception as e:
            print(f"   ❌ [SWARM MANAGER] Allocation Failed: {e}")
            self.flush_memory()
            return False


# ---------------------------------------------------------
# 2. THE SELF-REFLECTIVE AGENTIC OBSERVER
# ---------------------------------------------------------
def build_optimization_prompt(s, sy, p, snn_mean, haptic, mod, last_agent):
    return f"""SYSTEM STATE:
- Coherence (s): {s:.3f}
- Synchrony (sy): {sy:.3f}
- Phase (p): {p:.3f}
- Mean SNN spike: {snn_mean:.3f}
- Haptic level: {haptic:.3f}
- Modality: {mod}
- Current agent: {last_agent}

TASK:
Analyze the above state and output a JSON object with:
- "gain_multiplier": float (0.1-5.0)
- "entropy_injection": float (-0.2 to 0.2)
- "switch_model": string or null (Must be one of: "Qwen/Qwen2.5-0.5B-Instruct", "facebook/opt-125m", "Qwen/Qwen2-VL-2B-Instruct", null)
- "summary": string (max 10 words)

Provide ONLY the JSON object.
Example:
{{"gain_multiplier": 1.2, "entropy_injection": 0.05, "switch_model": null, "summary": "Stable, maintain current course"}}
"""

class LaptopAgenticSwarmObserver(BaseObserver):
    def __init__(self):
        super().__init__()
        self.manager = LaptopSwarmManager()
        self.history = []
        self.manager.load_agent("Qwen/Qwen2.5-0.5B-Instruct")
        print("🧠 [SELF-REFLECTIVE SWARM] Active. AI is now tuning its own engine parameters.")

    def evaluate(self, s, sy, p, snn, text="", haptic_level=0.0, **kwargs):
        self.history.append(s)
        if len(self.history) > 10: self.history.pop(0)

        snn_mean = np.mean(snn) if len(snn) else 0.5
        mod = kwargs.get('mod', 'TEXT')
        file_path = kwargs.get('file_path', None)
        last_agent = self.manager.active_model_name or "None"

        # --- Hard-Override for strict modality needs ---
        if mod == "IMAGE_NODE" or (file_path and file_path.endswith(('.png', '.jpg', '.jpeg'))):
            self.manager.load_agent("Qwen/Qwen2-VL-2B-Instruct", is_vision=True)
        elif mod == "AUDIO_NODE":
            self.manager.load_agent("openai/whisper-tiny", is_audio=True)
            
        # --- LLM Self-Reflection & Generation ---
        suggested_params = {}
        raw_output = "Processing..."
        
        prompt = build_optimization_prompt(s, sy, p, snn_mean, haptic_level, mod, last_agent)

        if self.manager.model and hasattr(self.manager, 'tokenizer') and not getattr(self, 'is_vision', False):
            try:
                inputs = self.manager.tokenizer(prompt, return_tensors="pt").to(self.manager.device)
                with torch.no_grad():
                    out = self.manager.model.generate(**inputs, max_new_tokens=80, do_sample=False)
                raw_output = self.manager.tokenizer.decode(out[0][inputs.input_ids.size(1):], skip_special_tokens=True).strip()
                
                # Regex to isolate JSON block
                json_match = re.search(r'\{.*\}', raw_output, re.DOTALL)
                if json_match:
                    suggested_params = json.loads(json_match.group())
            except Exception as e:
                pass # Fail silently, system will rely on inertia 

        # --- Apply AI-Suggested Parameters ---
        if 'gain_multiplier' in suggested_params:
            kwargs['gain_multiplier'] = np.clip(suggested_params['gain_multiplier'], 0.1, 5.0)
            
        if 'entropy_injection' in suggested_params:
            kwargs['entropy_injection'] = np.clip(suggested_params['entropy_injection'], -0.2, 0.2)
            
        if 'switch_model' in suggested_params and suggested_params['switch_model']:
            new_model = suggested_params['switch_model']
            if new_model != self.manager.active_model_name:
                self.manager.load_agent(new_model) 

        # Store the LLM's summary as the hallucination text for the UI
        kwargs['swarm_hallucination'] = suggested_params.get('summary', raw_output[:60].replace('\n', ' '))

        # The observer's resonance output
        return float(np.clip((s * 0.5) + (p * 0.5), 0.0, 1.0))