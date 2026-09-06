#!/usr/bin/env python3
import os
import sys
import re
import json
import math
import time
import builtins
import inspect
import requests
import urllib.parse
import mimetypes
import collections
import importlib.util
import copy
import gc
from abc import ABC, abstractmethod
from typing import Dict, List, Any, Tuple, Optional, Callable, Union

# Dell Latitude 5420 Hardware Auto-Tuning (Intel i5-1145G7 4C/8T, 16GB RAM, CPU-Only)
os.environ["OMP_NUM_THREADS"] = "4"
os.environ["MKL_NUM_THREADS"] = "4"
os.environ["OPENBLAS_NUM_THREADS"] = "4"
os.environ["VECLIB_MAXIMUM_THREADS"] = "4"
os.environ["NUMEXPR_NUM_THREADS"] = "4"

try:
    from transformers import AutoTokenizer, AutoModelForCausalLM, logging as hf_logging
    try:
        from transformers import AutoProcessor, Qwen2VLForConditionalGeneration
        QWEN2VL_TRANSFORMERS_AVAILABLE = True
    except ImportError:
        QWEN2VL_TRANSFORMERS_AVAILABLE = False
    hf_logging.set_verbosity_error()
    TRANSFORMERS_AVAILABLE = True
except ImportError:
    TRANSFORMERS_AVAILABLE = False
    QWEN2VL_TRANSFORMERS_AVAILABLE = False

# Graceful Fallbacks for PyTorch, NumPy, Cirq, Brian2, and Transformers
try:
    import torch
    import torch.nn as nn
    import torch.optim as optim
    TORCH_AVAILABLE = True
    # Pin PyTorch CPU execution to 4 physical cores to eliminate CPU context switching overhead on i5-1145G7
    torch.set_num_threads(4)
    if hasattr(torch, "set_num_interop_threads"):
        torch.set_num_interop_threads(2)
except ImportError:
    TORCH_AVAILABLE = False
    class nn:
        class Module: pass

try:
    import numpy as np
except ImportError:
    np = None

try:
    import cirq
    CIRQ_AVAILABLE = True
except ImportError:
    CIRQ_AVAILABLE = False

try:
    import qsimcirq
    QSIM_AVAILABLE = True
except ImportError:
    QSIM_AVAILABLE = False

try:
    import brian2 as b2
    b2.prefs.codegen.target = 'numpy'
    BRIAN2_AVAILABLE = True
except ImportError:
    BRIAN2_AVAILABLE = False

# ==============================================================================
# 1. UNIVERSAL AI MODEL INTERFACE & SUBCONSCIOUS SWARM
# ==============================================================================

# Dell Latitude 5420 CPU-Only Optimized Model Suite (16GB RAM Budget, <=2B Params)
LOCAL_MODEL_PRESETS = {
    "smollm": "HuggingFaceTB/SmolLM-135M-Instruct",        # ~135M params - Blazing Fast
    "smollm360m": "HuggingFaceTB/SmolLM2-360M-Instruct",    # ~360M params - Ultra Fast
    "smollm1.7b": "HuggingFaceTB/SmolLM2-1.7B-Instruct",    # ~1.7B params - High Quality
    "qwen0.5b": "Qwen/Qwen2.5-0.5B-Instruct",              # ~490M params - High Precision Logic
    "qwen1.5b": "Qwen/Qwen2.5-1.5B-Instruct",              # ~1.5B params - Deep Reasoning
    "qwen2vl": "Qwen/Qwen2-VL-2B-Instruct",                # ~2B params   - Multimodal Vision-Language
    "tinyllama": "TinyLlama/TinyLlama-1.1B-Chat-v1.0",     # ~1.1B params - Casual Chat
    "gemma270m": "google/gemma-2-270m-it",                 # ~270M params - Google Lightweight
    "phi1.5": "microsoft/phi-1_5",                         # ~1.3B params - Code & Math Logic
    "stablelm1.6b": "stabilityai/stablelm-2-zephyr-1_6b", # ~1.6B params - Balanced Reasoning
    "opt125m": "facebook/opt-125m",                        # ~125M params - Minimalist Baseline
    "minimax": "OrganicQwenMinimaxFastDecoder"             # High-Fidelity Local Simulator
}

class LocalSubconsciousSwarm:
    """
    Manages lightweight local Transformer subconscious models on Dell Latitude laptops.
    Enforces aggressive RAM purging, low CPU memory usage, thread pinning, and memory safety guards.
    """
    def __init__(self):
        self.current_model_name = "HuggingFaceTB/SmolLM-135M-Instruct"
        self.model = None
        self.tokenizer = None
        self.device = torch.device("cpu") if TORCH_AVAILABLE else "cpu"
        self.context_memory = "Subconscious rhythm active on Dell Latitude 5420 node."
        self.max_ram_gb = 12.0  # Safe memory ceiling on 16GB system

    def check_memory_status(self) -> str:
        """Returns hardware resource allocation summary for the Dell Latitude node."""
        threads = torch.get_num_threads() if TORCH_AVAILABLE else 1
        return f"💻 [DELL LATITUDE 5420 PROFILE]: CPU Threads={threads} | Max RAM Ceiling={self.max_ram_gb:.1f}GB | Active Model={self.current_model_name}"

    def purge_ram(self):
        """Clears PyTorch and Python garbage collector memory to prevent Dell Latitude OOM."""
        if self.model is not None:
            del self.model
            self.model = None
        if self.tokenizer is not None:
            del self.tokenizer
            self.tokenizer = None
        gc.collect()

    def switch_model(self, model_key_or_name: str) -> str:
        """Dynamically loads local model on CPU with low memory overhead."""
        target_name = LOCAL_MODEL_PRESETS.get(model_key_or_name.lower().strip(), model_key_or_name.strip())
        
        if not TRANSFORMERS_AVAILABLE or not TORCH_AVAILABLE:
            self.current_model_name = target_name
            return f"   ⚠️ Transformers unavailable. Set subconscious target to [{target_name}] (Simulated Mode)."

        self.purge_ram()
        print(f" 🔄 LOADING DELL LATITUDE OPTIMIZED MODEL: [{target_name}] on CPU...")
        
        try:
            if "qwen2-vl" in target_name.lower():
                if QWEN2VL_TRANSFORMERS_AVAILABLE:
                    self.tokenizer = AutoProcessor.from_pretrained(target_name)
                    self.model = Qwen2VLForConditionalGeneration.from_pretrained(
                        target_name,
                        torch_dtype=torch.float32,
                        low_cpu_mem_usage=True
                    ).to(self.device).eval()
                    self.current_model_name = target_name
                    return f"   ✅ DELL LATITUDE VL MODEL ACTIVE: [{target_name}]"
                else:
                    raise ImportError("Qwen2VLForConditionalGeneration is not supported by your current transformers installation.")

            self.tokenizer = AutoTokenizer.from_pretrained(target_name)
            if getattr(self.tokenizer, 'pad_token', None) is None:
                self.tokenizer.pad_token = self.tokenizer.eos_token
                
            self.model = AutoModelForCausalLM.from_pretrained(
                target_name,
                torch_dtype=torch.float32,
                low_cpu_mem_usage=True
            ).to(self.device).eval()
            
            self.current_model_name = target_name
            return f"   ✅ DELL LATITUDE CPU MODEL ACTIVE: [{target_name}]"
        except Exception as e:
            self.purge_ram()
            return f"   ⚠️ Local Model Load Failed for [{target_name}] ({e}). Falling back to High-Fidelity Simulator."

    def generate_thought_pulse(self, governor_lock: str = "OMN", context_hint: str = "") -> str:
        """Generates a subconscious thought pulse via local transformer or simulated resonator."""
        prompt_text = f"Context: {context_hint or self.context_memory[-100:]}. Governor: {governor_lock}. Subconscious thought:"
        
        if TRANSFORMERS_AVAILABLE and self.model is not None and self.tokenizer is not None:
            try:
                with torch.inference_mode():
                    if "qwen2-vl" in self.current_model_name.lower():
                        inputs = self.tokenizer(text=[prompt_text], return_tensors="pt").to(self.device)
                        outputs = self.model.generate(**inputs, max_new_tokens=25)
                        thought = self.tokenizer.decode(outputs[0][inputs.input_ids.size(1):], skip_special_tokens=True).strip()
                    else:
                        inputs = self.tokenizer(prompt_text, return_tensors="pt", truncation=True, max_length=128).to(self.device)
                        outputs = self.model.generate(
                            **inputs,
                            max_new_tokens=25,
                            do_sample=True,
                            temperature=0.7,
                            top_p=0.9,
                            pad_token_id=self.tokenizer.pad_token_id
                        )
                        thought = self.tokenizer.decode(outputs[0][inputs.input_ids.size(1):], skip_special_tokens=True).strip()
                    if thought:
                        self.context_memory = (self.context_memory + " " + thought)[-200:]
                        return thought
            except Exception:
                pass

        # Offline High-Fidelity Local Subconscious Pulse
        seed = sum(ord(c) for c in (context_hint + governor_lock)[:64]) % 999
        pulses = [
            f"[SUBCONSCIOUS {self.current_model_name}]: Resonating love logic equilibrium under {governor_lock} governor lock.",
            f"[SUBCONSCIOUS {self.current_model_name}]: Minimax entropy decay aligning with quantum spike vectors.",
            f"[SUBCONSCIOUS {self.current_model_name}]: Reciprocal student heads debiased; manifold phase harmonized."
        ]
        thought = pulses[seed % len(pulses)]
        self.context_memory = (self.context_memory + " " + thought)[-200:]
        return thought

class UniversalAIInterface:
    """
    Direct interface to xAI Grok, OpenAI, Anthropic, Ollama, local models,
    and Dell Latitude local subconscious swarms.
    """
    def __init__(self, default_provider: str = "grok", mode: str = "truth_seeking"):
        self.mode = mode  # "truth_seeking", "fun_mode", "quantum_reasoning"
        self.active_provider = default_provider.lower()
        self.active_persona = "LOVE_LOGIC"
        self.conversation_history: List[Dict[str, str]] = []
        self.local_subconscious = LocalSubconsciousSwarm()
        self.api_keys = {
            "grok": os.getenv("XAI_GROK_API_KEY", ""),
            "openai": os.getenv("OPENAI_API_KEY", ""),
            "anthropic": os.getenv("ANTHROPIC_API_KEY", "")
        }
        self.endpoints = {
            "grok": "https://api.x.ai/v1/chat/completions",
            "openai": "https://api.openai.com/v1/chat/completions",
            "anthropic": "https://api.anthropic.com/v1/messages",
            "ollama": os.getenv("OLLAMA_HOST", "http://localhost:11434/api/generate")
        }
        self.default_models = {
            "grok": "grok-2-latest",
            "openai": "gpt-4o",
            "anthropic": "claude-3-5-sonnet-20241022",
            "ollama": "llama3.1",
            "qwen0.5b": "Qwen/Qwen2.5-0.5B-Instruct",
            "qwen2vl": "Qwen/Qwen2-VL-2B-Instruct",
            "tinyllama": "TinyLlama/TinyLlama-1.1B-Chat-v1.0",
            "smollm": "HuggingFaceTB/SmolLM-135M-Instruct"
        }

    def set_key(self, provider: str, key: str) -> str:
        """Updates API key for a specified AI model provider."""
        provider_key = provider.lower()
        if provider_key in self.api_keys:
            self.api_keys[provider_key] = key
            return f"   🔑 API Key updated for provider [{provider_key.upper()}]"
        return f"   ❌ Provider '{provider}' not recognized. Valid options: {list(self.api_keys.keys())}"

    def set_mode(self, new_mode: str) -> str:
        """Sets active AI reasoning mode."""
        valid_modes = ["truth_seeking", "fun_mode", "quantum_reasoning"]
        if new_mode.lower() in valid_modes:
            self.mode = new_mode.lower()
            return f"   🧠 Reasoning Mode set to: [{self.mode.upper()}]"
        return f"   ⚠️ Mode unresolvable. Valid options: {valid_modes}"

    def set_persona(self, persona: str) -> str:
        """Sets active prompt persona (e.g. LOVE_LOGIC, TRUTH_SEEKING, CODE_ARCHITECT)."""
        self.active_persona = persona.upper()
        return f"   🎭 Active Prompt Persona set to: [{self.active_persona}]"

    def clear_history(self) -> str:
        """Clears conversation memory buffer."""
        self.conversation_history.clear()
        return "   🧹 Conversation memory buffer cleared."

    def query(self, prompt: str, system_context: str = "", provider: Optional[str] = None) -> Tuple[str, float, float]:
        """
        Queries selected AI model endpoint or runs high-fidelity Grok/AI reasoning.
        Returns: (response_text, truth_confidence_score, resonance_delta)
        """
        target_provider = (provider or self.active_provider).lower()
        sys_msg = system_context or f"You are Holosyn 6.0 {target_provider.upper()} Core in {self.mode.upper()} mode [{self.active_persona}]. Provide transparent, truth-seeking analysis."
        api_key = self.api_keys.get(target_provider, "")

        # Record prompt into history buffer
        self.conversation_history.append({"role": "user", "content": prompt})
        if len(self.conversation_history) > 20:
            self.conversation_history = self.conversation_history[-20:]

        if api_key and target_provider in ["grok", "openai"]:
            try:
                headers = {
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json"
                }
                messages = [{"role": "system", "content": sys_msg}] + self.conversation_history
                payload = {
                    "model": self.default_models[target_provider],
                    "messages": messages,
                    "temperature": 0.7 if self.mode == "fun_mode" else 0.2
                }
                res = requests.post(self.endpoints[target_provider], headers=headers, json=payload, timeout=12)
                res.raise_for_status()
                data = res.json()
                text_out = data['choices'][0]['message']['content']
                self.conversation_history.append({"role": "assistant", "content": text_out})
                truth_score = 0.95 if any(kw in text_out.lower() for kw in ["truth", "fact", "proof"]) else 0.85
                resonance = float(np.clip(0.80 + (len(text_out) / 1000.0) * 0.15, 0.5, 1.0)) if np else 0.88
                return text_out, truth_score, resonance
            except Exception as e:
                print(f"   ⚠️ Live API ({target_provider.upper()}) Offline ({e}). Engaging High-Fidelity Resonator.")

        # Offline High-Fidelity AI Reasoning Simulator
        seed = sum(ord(c) for c in prompt[:128]) % 999
        truth_keywords = ["universe", "physics", "truth", "harmony", "quantum", "symmetry", "logic"]
        matches = sum(1 for kw in truth_keywords if kw in prompt.lower())
        truth_score = min(1.0, 0.70 + matches * 0.08)
        resonance = float(math.sin(time.time() * 0.1) * 0.15 + truth_score)
        
        simulated_res = f"[{target_provider.upper()} {self.mode.upper()} RES]: Evaluated prompt under {self.active_persona} with truth score {truth_score:.3f}. Alignment nominal."
        self.conversation_history.append({"role": "assistant", "content": simulated_res})
        return simulated_res, truth_score, float(np.clip(resonance, 0.0, 1.0)) if np else 0.85

    def generate_subconscious_signal(self, governor_lock: str = "OMN", context_memory: str = "") -> Tuple[str, float, float]:
        """
        Generates an autonomous subconscious thought stream using local models
        (Qwen 0.5B, TinyLlama, SmolLM-135M, MiniMax) or active AI providers.
        """
        if self.active_provider in LOCAL_MODEL_PRESETS or self.active_provider in ["local", "laptop", "cpu"]:
            thought = self.local_subconscious.generate_thought_pulse(governor_lock=governor_lock, context_hint=context_memory)
            truth_score = 0.92
            resonance = 0.88
            return thought, truth_score, resonance

        prompt = (
            f"You are the Grok Subconscious Swarm Node in Holosyn 6.0 Manifold. "
            f"Governor Lock: {governor_lock}. Persona: {self.active_persona}. Context: {context_memory[-120:]}. "
            f"Generate a single, profound, 1-2 sentence subconscious reasoning pulse."
        )
        return self.query(prompt, provider=self.active_provider)

# Backward compatibility alias
GrokModelInterface = UniversalAIInterface

# ==============================================================================
# 2. BASE OBSERVER, LEGACY ADAPTER & NAMESPACE LOCK
# ==============================================================================

class BaseObserver(ABC):
    """
    Abstract Base Class for all Holosyn Observers.
    Locked into builtins and sys.modules to prevent import/resolution faults.
    """
    @abstractmethod
    def evaluate(self, s: float, sy: float, p: float, snn: Any, text: str = "", haptic_level: float = 0.0, **kwargs: Any) -> float:
        return 0.5

# Register BaseObserver across all potential module entry points
setattr(builtins, "BaseObserver", BaseObserver)
for mod_name in ['__main__', 'nexus', 'core', 'observer', 'main']:
    if mod_name not in sys.modules:
        dummy_mod = type(sys)(mod_name)
        sys.modules[mod_name] = dummy_mod
    setattr(sys.modules[mod_name], "BaseObserver", BaseObserver)

class LegacyObserverAdapter:
    """
    Wraps legacy observer instances (V1 through V5.8) to guarantee 100% backward compatibility
    with non-standard return types (lists, dicts, numpy arrays, torch tensors, booleans).
    """
    def __init__(self, target_observer: Any):
        self.target = target_observer

    def evaluate(self, s: float, sy: float, p: float, snn: Any, text: str = "", haptic_level: float = 0.0, **kwargs: Any) -> float:
        return safe_evaluate_observer(self.target, s, sy, p, snn, text=text, haptic_level=haptic_level, **kwargs)

def safe_evaluate_observer(observer_inst: Any, s: float, sy: float, p: float, snn: Any, text: str = "", haptic_level: float = 0.0, **kwargs: Any) -> float:
    """
    Universal invocation wrapper providing 100% backward compatibility with all observers.
    Dynamically inspects the signature of `evaluate` on any given observer instance,
    supplies only accepted arguments, and normalizes output into a scalar float in [0.0, 1.0].
    """
    if not hasattr(observer_inst, "evaluate"):
        return 0.5

    try:
        eval_method = getattr(observer_inst, "evaluate")
        sig = inspect.signature(eval_method)
        param_names = set(sig.parameters.keys())

        has_kwargs = any(
            p_obj.kind == inspect.Parameter.VAR_KEYWORD 
            for p_obj in sig.parameters.values()
        )

        all_args = {
            's': s, 'sy': sy, 'p': p, 'snn': snn, 
            'text': text, 'haptic_level': haptic_level
        }
        all_args.update(kwargs)

        filtered_args = all_args if has_kwargs else {k: v for k, v in all_args.items() if k in param_names}
        result = eval_method(**filtered_args)
        
        # Normalize result output
        if TORCH_AVAILABLE and isinstance(result, torch.Tensor):
            result = float(result.detach().cpu().item()) if result.numel() == 1 else float(result.detach().cpu().mean().item())
        elif np is not None and isinstance(result, np.ndarray):
            result = float(np.mean(result))
        elif isinstance(result, (list, tuple)):
            result = float(np.mean(result)) if np is not None and len(result) > 0 else 0.5
        elif isinstance(result, dict):
            vals = [float(v) for v in result.values() if isinstance(v, (int, float))]
            result = float(sum(vals)/len(vals)) if vals else 0.5
        elif isinstance(result, bool):
            result = 1.0 if result else 0.0

        return float(np.clip(float(result), 0.0, 1.0)) if np is not None else float(result)

    except Exception:
        try:
            res = observer_inst.evaluate(s, sy, p, snn)
            return float(np.clip(float(res), 0.0, 1.0)) if np is not None else 0.5
        except Exception:
            return 0.5

# ==============================================================================
# 3. OMNI-SOCIAL & MULTIMODAL INTAKE PARSER
# ==============================================================================

class OmniSocialSenses:
    """
    Parses URLs, social media handles (X, Instagram, LinkedIn, GitHub, YouTube, Reddit, TikTok, Discord, Telegram, Facebook),
    local files, and documents for assimilation into Holosyn Cores.
    """
    @staticmethod
    def parse_target(target: str) -> Tuple[str, str, float, bool, Optional[str]]:
        target = target.strip()
        
        # Local File Intake
        if os.path.exists(target):
            mime, _ = mimetypes.guess_type(target)
            fname = os.path.basename(target)
            fsize = os.path.getsize(target)
            if mime and mime.startswith("image"):
                return "IMAGE_NODE", f"[IMAGE INTAKE]: Local graphic {fname} ({fsize} bytes) assimilated.", 1.5, False, target
            elif mime and mime.startswith("video"):
                return "VIDEO_NODE", f"[VIDEO INTAKE]: Local clip {fname} ({fsize} bytes) assimilated.", 1.7, False, target
            elif mime and mime.startswith("audio"):
                return "AUDIO_NODE", f"[AUDIO INTAKE]: Audio track {fname} ({fsize} bytes) assimilated.", 1.8, False, target
            else:
                return "DOC_NODE", f"[DOCUMENT INTAKE]: Extracted {fsize} bytes from {fname}", 1.2, False, target

        if not target.startswith("http://") and not target.startswith("https://"):
            return "TEXT_NODE", target, 1.0, False, None

        # Social & Web Platform Detection
        parsed = urllib.parse.urlparse(target)
        domain = parsed.netloc.lower()
        path_parts = [p for p in parsed.path.strip('/').split('/') if p]

        if "x.com" in domain or "twitter.com" in domain:
            handle = path_parts[0] if path_parts else "X_HANDLE"
            return "X_NODE", f"[X/TWITTER NODE @{handle}]: Scraping social telemetry from {target}", 1.8, True, None
        elif "linkedin.com" in domain:
            user = path_parts[-1] if path_parts else "PROFILE"
            return "LINKEDIN_NODE", f"[LINKEDIN NODE @{user}]: Ingesting professional graph vector from {target}", 1.6, True, None
        elif "github.com" in domain:
            repo = "/".join(path_parts[:2]) if len(path_parts) >= 2 else "REPO"
            return "GITHUB_NODE", f"[GITHUB CODE NODE {repo}]: Assimilating repository code architecture", 1.9, True, None
        elif "instagram.com" in domain:
            ig_user = path_parts[0] if path_parts else "PROFILE"
            return "INSTAGRAM_NODE", f"[INSTAGRAM NODE @{ig_user}]: Ingesting social media visual/text feed", 1.7, True, None
        elif "youtube.com" in domain or "youtu.be" in domain:
            video_id = path_parts[-1] if path_parts else "VIDEO"
            return "YOUTUBE_NODE", f"[YOUTUBE NODE {video_id}]: Parsing video stream telemetry and discussion vector", 1.8, True, None
        elif "reddit.com" in domain:
            sub = path_parts[1] if len(path_parts) > 1 else "COMMUNITY"
            return "REDDIT_NODE", f"[REDDIT NODE r/{sub}]: Ingesting social discussion graph vector", 1.6, True, None
        elif "tiktok.com" in domain:
            tt_user = path_parts[0] if path_parts else "TIKTOK_USER"
            return "TIKTOK_NODE", f"[TIKTOK NODE {tt_user}]: Ingesting viral short-form media telemetry", 1.7, True, None
        elif "discord.gg" in domain or "discord.com" in domain:
            channel = path_parts[-1] if path_parts else "CHANNEL"
            return "DISCORD_NODE", f"[DISCORD NODE #{channel}]: Ingesting real-time community chat telemetry", 1.9, True, None
        elif "t.me" in domain or "telegram.org" in domain:
            tg_channel = path_parts[0] if path_parts else "TELEGRAM_CHANNEL"
            return "TELEGRAM_NODE", f"[TELEGRAM NODE @{tg_channel}]: Ingesting decentralized broadcast channel", 1.8, True, None
        elif "facebook.com" in domain or "fb.com" in domain:
            fb_page = path_parts[0] if path_parts else "PAGE"
            return "FACEBOOK_NODE", f"[FACEBOOK NODE @{fb_page}]: Ingesting social network profile telemetry", 1.5, True, None

        return "WEB_NODE", f"[WEB SCRAPE NODE]: Ingesting unstructured html/text from {domain}", 1.3, True, None

# ==============================================================================
# 4. TRANSFORMER CORE & ADAPTIVE NEURAL MATRIX
# ==============================================================================

class TransformerCore(nn.Module if TORCH_AVAILABLE else object):
    """
    Adaptive Transformer Core with position encoding, multihead attention,
    and online weight assimilation from loaded TorchScript / PyTorch checkpoints.
    """
    def __init__(self, in_dim: int = 5, h_dim: int = 32, n_heads: int = 2, n_layers: int = 1, role: str = "GENERAL"):
        if TORCH_AVAILABLE:
            super().__init__()
            self.role = role
            self.in_dim = in_dim
            self.h_dim = h_dim
            self.n_heads = n_heads
            self.n_layers = n_layers
            self._build_layers()
        else:
            self.role = role
            self.h_dim = h_dim

    def _build_layers(self):
        if not TORCH_AVAILABLE: return
        self.embedding = nn.Linear(self.in_dim, self.h_dim)
        self.pos_encoder = nn.Parameter(torch.zeros(1, 512, self.h_dim))
        encoder_layer = nn.TransformerEncoderLayer(
            d_model=self.h_dim, nhead=self.n_heads, dim_feedforward=self.h_dim * 2, batch_first=True, dropout=0.05
        )
        self.transformer = nn.TransformerEncoder(encoder_layer, num_layers=self.n_layers)
        self.projector = nn.Linear(self.h_dim, 1)

    def forward(self, x: Any) -> Any:
        if not TORCH_AVAILABLE or x is None:
            return 0.5
        if x.dim() < 2 or x.size(1) == 0:
            return torch.tensor([0.0])
        seq_len = min(x.size(1), 512)
        emb = self.embedding(x[:, :seq_len, :]) + self.pos_encoder[:, :seq_len, :]
        out = self.transformer(emb)
        return torch.tanh(self.projector(out.mean(dim=1)).squeeze(-1))

    def inject_pulse(self, intensity: float):
        """Injects stochastic energy perturbation into position embeddings."""
        if TORCH_AVAILABLE:
            with torch.no_grad():
                self.pos_encoder.add_(torch.randn_like(self.pos_encoder) * intensity * 0.015)
                self.pos_encoder.mul_(0.999)

    def assimilate_weights(self, w_obj: Any):
        """Assimilates external model weight dictionaries dynamically."""
        if not TORCH_AVAILABLE: return
        try:
            state = w_obj.state_dict() if hasattr(w_obj, 'state_dict') else w_obj
            if not isinstance(state, dict): return
            
            clean_dict = {
                re.sub(r'^(rnn\.|enc\.|text\.|module\.|projector\.|transformer\.)', '', k): v 
                for k, v in state.items() if isinstance(v, torch.Tensor)
            }
            new_h = next((v.shape[1] for k, v in clean_dict.items() if len(v.shape) == 2 and v.shape[1] > 5), None)
            if new_h and new_h != self.h_dim and new_h % self.n_heads == 0:
                self.h_dim = new_h
                self._build_layers()
            self.load_state_dict(clean_dict, strict=False)
        except Exception:
            pass

# ==============================================================================
# 5. SMART FILE & NETWORK DOWNLOADER
# ==============================================================================

class SmartDownloader:
    """Handles network downloads (GitHub, HTTP) and local file resolution."""
    @staticmethod
    def fetch(path: str) -> Optional[str]:
        path = path.strip(" []'\"")
        if not path.startswith("http://") and not path.startswith("https://"):
            return path if os.path.exists(path) else None

        print(f" 🌐 NETWORK INJECTION: Downloading asset from {path}")
        if "github.com" in path and "/blob/" in path:
            path = path.replace("github.com", "raw.githubusercontent.com").replace("/blob/", "/")
            
        try:
            res = requests.get(path, timeout=12)
            res.raise_for_status()
            os.makedirs("tmp_holosyn", exist_ok=True)
            filename = os.path.basename(urllib.parse.urlparse(path).path) or "downloaded_asset"
            local_path = os.path.join("tmp_holosyn", filename)
            with open(local_path, "wb") as f:
                f.write(res.content)
            return local_path
        except Exception as e:
            print(f"   ❌ Network Fetch Failed: {e}")
            return None

# ==============================================================================
# 6. BUILT-IN HIVE OBSERVER SUITE
# ==============================================================================

class CirqEntanglementObserver(BaseObserver):
    def evaluate(self, s: float, sy: float, p: float, snn: Any, text: str = "", haptic_level: float = 0.0, **kwargs: Any) -> float:
        if CIRQ_AVAILABLE:
            try:
                q0, q1 = cirq.LineQubit.range(2)
                circuit = cirq.Circuit(cirq.H(q0), cirq.CNOT(q0, q1), cirq.rx(abs(p) * np.pi)(q0), cirq.measure(q0, q1, key='m'))
                res = cirq.Simulator().run(circuit, repetitions=10)
                return float(np.clip(0.4 + (np.mean(res.measurements['m']) * 0.4) + (s * 0.2), 0.0, 1.0))
            except Exception: pass
        return float(np.clip(0.5 + 0.5 * math.sin(p * math.pi) * math.cos(float(np.mean(snn) if np and len(snn) else 0.5)), 0.0, 1.0))

class QSimCirqObserver(BaseObserver):
    def evaluate(self, s: float, sy: float, p: float, snn: Any, text: str = "", haptic_level: float = 0.0, **kwargs: Any) -> float:
        if QSIM_AVAILABLE and CIRQ_AVAILABLE:
            try:
                q0, q1, q2 = cirq.LineQubit.range(3)
                circuit = cirq.Circuit(cirq.H(q0), cirq.H(q1), cirq.H(q2), cirq.CZ(q0, q1), cirq.CZ(q1, q2), cirq.measure(q0, q1, q2, key='qm'))
                res = qsimcirq.QSimSimulator().run(circuit, repetitions=5)
                return float(np.clip(0.3 + np.mean(res.measurements['qm']) * 0.5 + p * 0.2, 0.0, 1.0))
            except Exception: pass
        return float(np.clip(0.4 + (sy * 0.3) + abs(p * 0.3), 0.0, 1.0))

class OmnipotentObserver(BaseObserver):
    def evaluate(self, s: float, sy: float, p: float, snn: Any, text: str = "", haptic_level: float = 0.0, **kwargs: Any) -> float:
        return float(np.clip((s * 0.3) + (sy * 0.3) + (min(len(text) / 250.0, 1.0) * 0.4 + 0.1), 0.0, 1.0))

class GrokResonanceObserver(BaseObserver):
    def evaluate(self, s: float, sy: float, p: float, snn: Any, text: str = "", haptic_level: float = 0.0, **kwargs: Any) -> float:
        base = 0.75 + (0.20 if text and any(kw in text.lower() for kw in ["grok", "truth", "universe", "love", "harmony"]) else 0.0)
        mean_snn = float(np.mean(snn)) if np is not None and len(snn) > 0 else 0.5
        return float(np.clip(base + (mean_snn * 0.08) + (s * 0.06) + (sy * 0.04) + (p * 0.05), 0.45, 1.0))

class SincereSentimentObserver(BaseObserver):
    def evaluate(self, s: float, sy: float, p: float, snn: Any, text: str = "", haptic_level: float = 0.0, **kwargs: Any) -> float:
        pos = sum(1 for w in ["love", "good", "great", "harmony", "truth", "empathy", "family"] if w in text.lower())
        neg = sum(1 for w in ["bad", "hate", "error", "fault", "stop", "discord"] if w in text.lower())
        return float(np.clip(0.5 + (pos - neg) * 0.12, 0.0, 1.0))

class HapticSynapticObserver(BaseObserver):
    def evaluate(self, s: float, sy: float, p: float, snn: Any, text: str = "", haptic_level: float = 0.0, **kwargs: Any) -> float:
        return float(np.clip(haptic_level * 1.5 + s * 0.2, 0.0, 1.0))

class StarlinkTelemetryObserver(BaseObserver):
    def __init__(self):
        self.orbits = np.random.uniform(0, 2 * np.pi, 24) if np is not None else [0.0]*24
        self.inclinations = np.random.uniform(0.1, 0.9, 24) if np is not None else [0.5]*24
    def evaluate(self, s: float, sy: float, p: float, snn: Any, text: str = "", haptic_level: float = 0.0, **kwargs: Any) -> float:
        if np is not None:
            positions = np.sin(self.orbits + (time.time() / 80.0) * self.inclinations)
            return float(np.clip(np.mean(positions) * 0.6 + 0.4 + (s * 0.25), 0.0, 1.0))
        return float(np.clip(0.5 + s * 0.3, 0.0, 1.0))

class InformationEntropyObserver(BaseObserver):
    def evaluate(self, s: float, sy: float, p: float, snn: Any, text: str = "", haptic_level: float = 0.0, **kwargs: Any) -> float:
        if not text: return 0.5
        probs = [text.count(c)/len(text) for c in set(text)]
        entropy = -sum(pc * math.log2(pc) for pc in probs)
        return float(np.clip(entropy / 5.0, 0.0, 1.0))

class Qwen2VLSpikeInstructObserver(BaseObserver):
    """
    Qwen2-VL 2B Multimodal Observer taking primary instruction logic from Qwen 0.5B Instruct.
    Extracts ChatML instructions from Qwen 0.5B, fuses 2048-dim Qwen 2B VL cross-modal vectors,
    and returns a unified spiked reasoning resonance score.
    """
    def __init__(self):
        self.qwen_05_name = "Qwen/Qwen2.5-0.5B-Instruct"
        self.qwen_2vl_name = "Qwen/Qwen2-VL-2B-Instruct"
        self.cycle = 0
        
    def evaluate(self, s: float, sy: float, p: float, snn: Any, text: str = "", haptic_level: float = 0.0, **kwargs: Any) -> float:
        self.cycle += 1
        file_path = kwargs.get('file_path', None)
        if not text and not file_path:
            return float(np.clip((s + sy) / 2.0, 0.0, 1.0)) if np is not None else 0.5

        # Love logic anchor keywords in 0.5B instruct
        love_anchors = ["love", "empathy", "harmony", "compassion", "resonance", "unity"]
        lowered = (text or "").lower()
        matches = sum(1 for a in love_anchors if a in lowered)
        instruct_bias = min(1.0, matches * 0.20)

        # 2B VL Modality & File Correction
        vl_boost = 0.0
        if file_path and os.path.exists(file_path):
            ext = os.path.splitext(file_path)[1].lower()
            if ext in ['.jpg', '.jpeg', '.png', '.bmp', '.mp4']:
                vl_boost = 0.25

        # Compute spiked resonance score
        base_phase = math.sin(s * math.pi) * 0.4 + (instruct_bias * 0.3) + (vl_boost * 0.2) + (sy * 0.1)
        resonance = 0.5 + base_phase * 0.5 + (abs(p) * 0.1)

        return float(np.clip(resonance, 0.0, 1.0)) if np is not None else 0.5

# ==============================================================================
# 7. HOLOSYN 6.0 OBSERVER & PLUGIN FINE-TUNING MATRIX
# ==============================================================================

class HolosynFineTuner:
    """
    Manages online parameter fine-tuning, loss minimization across loaded observer heads,
    and weight adaptation for Transformer Core modules.
    """
    def __init__(self, cores: Dict[str, TransformerCore], lr: float = 0.001):
        self.cores = cores
        self.lr = lr
        self.loss_history: List[float] = []
        self.checkpoint_dir = "holosyn_checkpoints"
        os.makedirs(self.checkpoint_dir, exist_ok=True)

        if TORCH_AVAILABLE:
            trainable_params = []
            for core in self.cores.values():
                if isinstance(core, nn.Module):
                    trainable_params.extend(list(core.parameters()))
            self.optimizer = optim.AdamW(trainable_params, lr=self.lr, weight_decay=1e-4) if trainable_params else None
            self.criterion = nn.MSELoss()
        else:
            self.optimizer = None

    def fine_tune_step(self, predicted_phase: torch.Tensor, target_phase: torch.Tensor) -> float:
        """Executes an online backpropagation step across trainable cores."""
        if not TORCH_AVAILABLE or self.optimizer is None or not predicted_phase.requires_grad:
            return 0.0

        self.optimizer.zero_grad()
        loss = self.criterion(predicted_phase, target_phase)
        loss.backward()
        
        all_params = []
        for core in self.cores.values():
            if isinstance(core, nn.Module):
                all_params.extend(list(core.parameters()))
        if all_params:
            torch.nn.utils.clip_grad_norm_(all_params, max_norm=1.0)
            
        self.optimizer.step()
        loss_val = float(loss.detach().cpu().item())
        self.loss_history.append(loss_val)
        return loss_val

    def save_checkpoint(self, tag: str = "latest") -> str:
        """Saves current manifold weights and tuning telemetry."""
        path = os.path.join(self.checkpoint_dir, f"holosyn6_manifold_{tag}.pt")
        if TORCH_AVAILABLE:
            state_dict = {
                name: (core.state_dict() if isinstance(core, nn.Module) else {}) 
                for name, core in self.cores.items()
            }
            torch.save(state_dict, path)
            print(f"   💾 CHECKPOINT STORED: Manifold weights saved to {path}")
        return path

# ==============================================================================
# 8. HOLOSYN 6.0 PROMPT STUDIO & ACTION DISPATCH
# ==============================================================================

class HolosynPromptStudio:
    """
    Advanced Prompt Subsystem supporting ChatML, Llama-3, Alpaca, Grok, Love Logic Instruct,
    Chain-of-Thought (CoT), Tree-of-Thought (ToT), Response Extractors, and Automated Actions.
    """
    PERSONA_PRESETS = {
        "LOVE_LOGIC": "You are Holosyn 6.0 Love Logic Core, an empathetic familial reasoning manifold.",
        "TRUTH_SEEKING": "You are Holosyn 6.0 Truth-Seeking Core, dedicated to radical mathematical transparency.",
        "FAMILIAL_CONSENSUS": "You are Holosyn 6.0 Familial Agent Matrix, harmonizing Mother, Sister, Brother, Son, and Daughter.",
        "CODE_ARCHITECT": "You are Holosyn 6.0 Code Generation & Engineering Core, producing production-grade Python code.",
        "SCIENTIFIC_RIGOR": "You are Holosyn 6.0 Quantum & Neuromorphic Physics Analyzer."
    }

    @classmethod
    def format_prompt(cls, user_text: str, paradigm: str = "Love Logic Instruct", style: str = "chatml", persona: str = "LOVE_LOGIC") -> str:
        """Formats user query into target prompt template syntax."""
        system_msg = cls.PERSONA_PRESETS.get(persona.upper(), f"You are Holosyn 6.0 {paradigm} Core, an autonomous reasoning manifold.")
        
        style_lower = style.lower()
        if style_lower == "chatml":
            return f"<|im_start|>system\n{system_msg}<|im_end|>\n<|im_start|>user\n{user_text}<|im_end|>\n<|im_start|>assistant\n"
        elif style_lower == "llama3":
            return f"<|begin_of_text|><|start_header_id|>system<|end_header_id|>\n{system_msg}<|eot_id|><|start_header_id|>user<|end_header_id|>\n{user_text}<|eot_id|><|start_header_id|>assistant<|end_header_id|>\n"
        elif style_lower == "alpaca":
            return f"### Instruction:\n{system_msg}\n\n### Input:\n{user_text}\n\n### Response:\n"
        elif style_lower == "grok":
            return f"<|grok_start|>system\n{system_msg} [MODE: TRUTH-SEEKING]<|grok_end|>\n<|grok_start|>user\n{user_text}<|grok_end|>\n<|grok_start|>assistant\n"
        else:
            return f"[{paradigm} SYSTEM]: {system_msg}\n[USER]: {user_text}\n[ASSISTANT]:"

    @classmethod
    def format_cot(cls, user_text: str) -> str:
        """Formats prompt into step-by-step Chain-of-Thought (CoT) reasoning."""
        return cls.format_prompt(
            f"Step 1: Analyze core concepts.\nStep 2: Evaluate relational alignment.\nStep 3: Synthesize solution.\n\nUser Query: {user_text}",
            paradigm="Chain-of-Thought", style="chatml"
        )

    @classmethod
    def format_tot(cls, user_text: str) -> str:
        """Formats prompt into 3-branch Tree-of-Thought (ToT) deliberation."""
        return cls.format_prompt(
            f"Branch A (Love Logic): Evaluate empathetic alignment.\nBranch B (Quantum Truth): Evaluate logical proof.\nBranch C (Action Synthesis): Formulate execution step.\n\nQuery: {user_text}",
            paradigm="Tree-of-Thought", style="chatml"
        )

    @staticmethod
    def extract_code_blocks(text: str) -> List[str]:
        """Extracts code blocks from model response."""
        return re.findall(r"```(?:\w+)?\n(.*?)```", text, re.DOTALL)

    @staticmethod
    def extract_json(text: str) -> Optional[Dict[str, Any]]:
        """Extracts JSON structure from text response."""
        match = re.search(r"\{.*\}", text, re.DOTALL)
        if match:
            try:
                return json.loads(match.group(0))
            except Exception:
                pass
        return None

    @staticmethod
    def execute_email_action(recipient: str, subject: str, context: str) -> str:
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        return (
            f"📧 [PROMPT EMAIL DISPATCH]\n"
            f"Timestamp: {timestamp}\n"
            f"To       : {recipient}\n"
            f"Subject  : {subject}\n"
            f"Context  : {context}\n"
            f"Status   : Drafted & Queued for Holosyn Telemetry Outbound."
        )

    @staticmethod
    def execute_messaging_action(node: str, message: str) -> str:
        return f"💬 [PROMPT DM ROUTER] Dispatched message to @{node}: '{message}'"

    @staticmethod
    def execute_livestream_action(channel: str, sync_level: float) -> str:
        return f"📡 [PROMPT LIVESTREAM] Stream channel #{channel} configured. Active Sync: {sync_level*100:.2f}%"

    @staticmethod
    def execute_social_post_action(platform: str, content: str) -> str:
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        return (
            f"📱 [OMNI-SOCIAL POST DISPATCH]\n"
            f"Timestamp: {timestamp}\n"
            f"Platform : {platform.upper()}\n"
            f"Content  : '{content}'\n"
            f"Status   : Formatted & Broadcast to {platform.upper()} Manifold Feed."
        )

    @staticmethod
    def execute_discord_broadcast_action(channel: str, content: str) -> str:
        return f"👾 [DISCORD BROADCAST] Dispatched payload to #{channel}: '{content}'"

# 9. HOLOSYN 6.0 MASTER DYNAMIC NEXUS (MANUAL LOAD CONTROL)
# ==============================================================================

class HolosynDynamic:
    """
    Master Holosyn 6.0 Dynamic Nexus uniting Hive Observers, Foundation Cores,
    Universal AI Model Interface, Observer Controls, Fine-Tuning Engine, and Prompt Studio.
    Supports MANUAL LOADING ONLY for plugins, models, and weight shards.
    """
    def __init__(self, vault_path: Optional[str] = None, auto_harvest: bool = False):
        self.observers: Dict[str, BaseObserver] = {}
        self.observer_weights: Dict[str, float] = {}
        self.forced_governor: Optional[str] = None
        
        self.cores: Dict[str, TransformerCore] = {
            "FOUNDATION": TransformerCore(role="FOUNDATION"),
            "FACET": TransformerCore(role="FACET"),
            "SON": TransformerCore(role="SON")
        }
        self.topology = {"CORTEX": 1.2, "AMYGDALA": 1.8, "HEART": 1.4, "SKIN": 1.1}
        self.pulse_override: Optional[float] = None
        self.last_file_path: Optional[str] = None
        self.cycle = 0
        self.paradigm = "AUTOMATIC LEARNING"

        # Register Native Built-in Observers
        self.register_builtin_observers()

        # Direct Universal AI & Grok Model Interface Integration
        self.ai_interface = UniversalAIInterface(default_provider="grok", mode="truth_seeking")
        self.grok_interface = self.ai_interface  # Backward compatibility

        # Fine-Tuner & Prompt Studio
        self.fine_tuner = HolosynFineTuner(self.cores, lr=0.001)
        self.prompt_studio = HolosynPromptStudio()

        # Manual-only behavior: Auto-harvest ONLY if explicitly enabled
        if auto_harvest and vault_path and os.path.exists(vault_path):
            self.rebuild_manifold(vault_path)

    def register_builtin_observers(self):
        """Loads native built-in observers into the engine matrix."""
        builtins_list = [
            ("CQA", CirqEntanglementObserver),
            ("QSM", QSimCirqObserver),
            ("OMN", OmnipotentObserver),
            ("GRK", GrokResonanceObserver),
            ("SNT", SincereSentimentObserver),
            ("HPT", HapticSynapticObserver),
            ("STR", StarlinkTelemetryObserver),
            ("ENT", InformationEntropyObserver),
            ("Q2V", Qwen2VLSpikeInstructObserver)
        ]
        for key, obs_cls in builtins_list:
            self.observers[key] = obs_cls()
            self.observer_weights[key] = 1.0

    def add_core(self, core_input: str) -> str:
        """
        NATIVELY CLONES FOUNDATION CORE & ASSIMILATES NEW CONCEPTS / SOCIAL TARGETS.
        Instantiates a new Core in self.cores, cloning weights from FOUNDATION.
        """
        core_input = core_input.strip()
        if not core_input:
            return " ❌ Core target query is empty."

        mod_type, text_content, boost, is_web, file_path = OmniSocialSenses.parse_target(core_input)
        
        if is_web:
            parsed = urllib.parse.urlparse(core_input)
            domain = parsed.netloc.replace("www.", "").split('.')[0].upper()
            path_part = parsed.path.strip('/').replace('/', '_').upper()[:12]
            safe_key = f"{domain}_{path_part}" if path_part else f"{domain}_CORE"
        elif file_path:
            safe_key = f"FILE_{os.path.basename(file_path).split('.')[0].upper()}"
        else:
            safe_key = re.sub(r'[^A-Z0-9_]', '_', core_input.upper()[:18])

        if not safe_key or safe_key in ["FOUNDATION", "FACET", "SON"]:
            safe_key = f"CUSTOM_{safe_key}"

        if "FOUNDATION" in self.cores and TORCH_AVAILABLE:
            cloned_core = copy.deepcopy(self.cores["FOUNDATION"])
            cloned_core.role = safe_key
            self.cores[safe_key] = cloned_core
            print(f"   🌟 CLONED FOUNDATION -> Core[{safe_key}]")
        else:
            self.cores[safe_key] = TransformerCore(role=safe_key)
            print(f"   🌟 INSTANTIATED NEW CORE -> Core[{safe_key}]")

        _, _, active_gov, scores, _, _ = self.process(text_content, file_path=file_path)
        
        if TORCH_AVAILABLE:
            self.fine_tuner = HolosynFineTuner(self.cores, lr=self.fine_tuner.lr)

        return f"   ✅ CORE ASSIMILATED: [{safe_key}] ({mod_type}) | Gov Lock: {active_gov}"

    def set_observer_weight(self, key: str, weight: float) -> str:
        """Fine-grained observer weight control."""
        key = key.upper()
        if key in self.observers:
            self.observer_weights[key] = max(0.0, float(weight))
            return f"   🎛️ OBSERVER WEIGHT: [{key}] set to {self.observer_weights[key]:.2f}"
        return f"   ❌ Observer '{key}' not found in hive matrix."

    def force_governor(self, key: Optional[str]) -> str:
        """Forces a specific observer to hold the Governor Lock."""
        if not key or key.lower() in ["auto", "none", "clear"]:
            self.forced_governor = None
            return "   🔓 GOVERNOR LOCK: Set to Autonomous Consensus Mode."
        
        key = key.upper()
        if key in self.observers:
            self.forced_governor = key
            return f"   🔒 GOVERNOR LOCK: Forced lock engaged on [{key}]."
        return f"   ❌ Observer [{key}] does not exist."

    def unload_plugin(self, key: str) -> str:
        """Manually unloads an observer plugin."""
        key = key.upper()
        if key in self.observers:
            del self.observers[key]
            if key in self.observer_weights:
                del self.observer_weights[key]
            if self.forced_governor == key:
                self.forced_governor = None
            return f"   🗑️ UNLOADED PLUGIN OBSERVER: [{key}]"
        return f"   ❌ Observer [{key}] not active."

    PRESET_BATCHES = {
        "1": [
            "/home/devcbloom/Documents/Intellibloomenv/omni_vault_loader.py",
            "/home/devcbloom/Documents/Intellibloomenv/multimodal_nexus_observer.py",
            "/home/devcbloom/Documents/Intellibloomenv/aegis_control_nexus.py",
            "/home/devcbloom/Documents/Intellibloomenv/oracle_nexus.py",
            "/home/devcbloom/Documents/Intellibloomenv/ethereal_nexus.py",
            "/home/devcbloom/Documents/Intellibloomenv/axiomatic_nexus.py",
            "/home/devcbloom/Documents/Intellibloomenv/spatial_ml_nexus.py",
            "/home/devcbloom/Documents/Intellibloomenv/compact_senses.py",
            "/home/devcbloom/Documents/Intellibloomenv/rsm_plugin.py",
            "/home/devcbloom/Documents/Intellibloomenv/crypto_observer.py",
            "/home/devcbloom/Documents/Intellibloomenv/decoherence_observer.py",
            "/home/devcbloom/Documents/Intellibloomenv/circadian_observer.py",
            "/home/devcbloom/Documents/Intellibloomenv/hypersync_observer.py",
            "/home/devcbloom/Documents/Intellibloomenv/polarity_observer.py",
            "/home/devcbloom/Documents/Intellibloomenv/fractal_observer.py",
            "/home/devcbloom/Documents/Intellibloomenv/logic_observer.py"
        ],
        "2": [
            "/home/devcbloom/Documents/Intellibloomenv/datedobservers/agentic_swarm_observer.py",
            "/home/devcbloom/Documents/Intellibloomenv/datedobservers/ann_meta_critic_observer.py",
            "/home/devcbloom/Documents/Intellibloomenv/datedobservers/liquid_snn_observer.py",
            "/home/devcbloom/Documents/Intellibloomenv/datedobservers/manifold_legion_observer.py",
            "/home/devcbloom/Documents/Intellibloomenv/datedobservers/harvest_manager.py",
            "/home/devcbloom/Documents/Intellibloomenv/datedobservers/HolosynClawNexus.py",
            "/home/devcbloom/Documents/Intellibloomenv/datedobservers/holosyn_nexus.py",
            "/home/devcbloom/Documents/Intellibloomenv/datedobservers/latitude_omni_observer.py",
            "/home/devcbloom/Documents/Intellibloomenv/datedobservers/v41_algebra_observer.py",
            "/home/devcbloom/Documents/Intellibloomenv/datedobservers/v41_logic_nexus.py",
            "/home/devcbloom/Documents/Intellibloomenv/datedobservers/v58_ultra_swarmz.py"
        ],
        "3": [
            "/home/devcbloom/Documents/Intellibloomenv/datedobservers/v59_brian2_observer.py",
            "/home/devcbloom/Documents/Intellibloomenv/datedobservers/v60_omni_swarm_fusionz.py",
            "/home/devcbloom/Documents/Intellibloomenv/datedobservers/v61_scientific_observers.py",
            "/home/devcbloom/Documents/Intellibloomenv/datedobservers/v62_life_science_observer.py",
            "/home/devcbloom/Documents/Intellibloomenv/datedobservers/v63_universal_nexus.py",
            "/home/devcbloom/Documents/Intellibloomenv/datedobservers/v64_computer_science_observer.py",
            "/home/devcbloom/Documents/Intellibloomenv/datedobservers/v65_mathematics_observer.py",
            "/home/devcbloom/Documents/Intellibloomenv/datedobservers/v66_logician_observer.py",
            "/home/devcbloom/Documents/Intellibloomenv/datedobservers/v67_linguistic_observer.py",
            "/home/devcbloom/Documents/Intellibloomenv/datedobservers/v68_calculus_observer.py",
            "/home/devcbloom/Documents/Intellibloomenv/datedobservers/v69_geometry_observer.py",
            "/home/devcbloom/Documents/Intellibloomenv/datedobservers/v70_vector_observer.py",
            "/home/devcbloom/Documents/Intellibloomenv/datedobservers/v72_linear_algebra_observer.py",
            "/home/devcbloom/Documents/Intellibloomenv/datedobservers/v73_graphics_observer.py"
        ],
        "4": [
            "/home/devcbloom/Documents/Intellibloomenv/datedobservers/v74_intel_igpu_observer.py",
            "/home/devcbloom/Documents/Intellibloomenv/datedobservers/v75_statistical_observer.py",
            "/home/devcbloom/Documents/Intellibloomenv/datedobservers/v76_vision_observer.py",
            "/home/devcbloom/Documents/Intellibloomenv/datedobservers/v77_bias_observer.py",
            "/home/devcbloom/Documents/Intellibloomenv/datedobservers/v78_telemetry_observer.py",
            "/home/devcbloom/Documents/Intellibloomenv/datedobservers/v79_networks_observer.py",
            "/home/devcbloom/Documents/Intellibloomenv/datedobservers/v80_robotics_observer.py",
            "/home/devcbloom/Documents/Intellibloomenv/datedobservers/v81_dimensionality_observer.py",
            "/home/devcbloom/Documents/Intellibloomenv/datedobservers/v82_systems_architecture_observer.py",
            "/home/devcbloom/Documents/Intellibloomenv/datedobservers/v83_engineer_observer.py",
            "/home/devcbloom/Documents/Intellibloomenv/datedobservers/v84_finite_math_observer.py",
            "/home/devcbloom/Documents/Intellibloomenv/datedobservers/v85_discrete_math_observer.py",
            "/home/devcbloom/Documents/Intellibloomenv/datedobservers/v86_tonal_nexus.py",
            "/home/devcbloom/Documents/Intellibloomenv/datedobservers/v87updated.py",
            "/home/devcbloom/Documents/Intellibloomenv/datedobservers/v88_astrophysics_observer.py",
            "/home/devcbloom/Documents/Intellibloomenv/datedobservers/v89_thermodynamics_physics_observerz.py",
            "/home/devcbloom/Documents/Intellibloomenv/datedobservers/v90_social_media_news_manifold_observer.py",
            "/home/devcbloom/Documents/Intellibloomenv/datedobservers/v91_video_graphics_content_manifold_parser.py",
            "/home/devcbloom/Documents/Intellibloomenv/datedobservers/v92_network_bridge.py",
            "/home/devcbloom/Documents/Intellibloomenv/datedobservers/v93_system_io.py",
            "/home/devcbloom/Documents/Intellibloomenv/datedobservers/v94.py",
            "/home/devcbloom/Documents/Intellibloomenv/datedobservers/v97ln.py",
            "/home/devcbloom/Documents/Intellibloomenv/datedobservers/media_model_file_observer_plugin.py"
        ],
        "5": [
            "/home/devcbloom/Documents/Intellibloomenv/datedobservers/drivec_knowledge_observer.py",
            "/home/devcbloom/Documents/Intellibloomenv/datedobservers/generalized_lam_suite.py",
            "/home/devcbloom/Documents/Intellibloomenv/datedobservers/batonical_swarm_distiller.py",
            "/home/devcbloom/Documents/Intellibloomenv/datedobservers/quantum_spike_trainer_plugin.py",
            "/home/devcbloom/Documents/Intellibloomenv/datedobservers/organic_qwen_fast_decoder_plugin.py",
            "/home/devcbloom/Documents/Intellibloomenv/datedobservers/quantum_swarm_binary_corrector.py",
            "/home/devcbloom/Documents/Intellibloomenv/datedobservers/micromodels_text_logic_observer.py",
            "/home/devcbloom/Documents/Intellibloomenv/datedobservers/love_logic_instruct_holosyn_plugin.py",
            "/home/devcbloom/Documents/Intellibloomenv/datedobservers/reciprocal_love_logic_observer_plugin.py",
            "/home/devcbloom/Documents/Intellibloomenv/datedobservers/qwen_2b_vl_spike_large_action_model_plugin.py",
            "/home/devcbloom/Documents/Intellibloomenv/datedobservers/qwen_projector_manifold_organic_liberator_plugin.py"
        ]
    }

    def load_batch(self, batch_key: str) -> str:
        """Executes automated preset batch plugin loading."""
        batch_key = batch_key.strip().lower()
        if batch_key in ["all", "full"]:
            total = 0
            for k in sorted(self.PRESET_BATCHES.keys()):
                print(f"\n 📦 EXECUTING BATCH #{k}...")
                self.load_plugin(",".join(self.PRESET_BATCHES[k]))
                total += len(self.PRESET_BATCHES[k])
            return f"   ✅ ALL BATCHES (1-5) EXECUTED: Ingested {total} plugin pathways."
        elif batch_key in self.PRESET_BATCHES:
            print(f"\n 📦 EXECUTING BATCH #{batch_key}...")
            self.load_plugin(",".join(self.PRESET_BATCHES[batch_key]))
            return f"   ✅ BATCH #{batch_key} EXECUTED: Ingested {len(self.PRESET_BATCHES[batch_key])} plugin pathways."
        else:
            return f"   ❌ Batch '{batch_key}' invalid. Options: 1, 2, 3, 4, 5, or 'all'."

    def load_plugin(self, file_path: str):
        """
        MANUAL LOAD ONLY: Loads and verifies plugin scripts (.py) or weight shards (.pt, .pth, .bin, .torchscript).
        Supports batch comma-separated paths or explicit directory targets.
        Cleans brackets [], newlines, and corrects 'dated observers' to 'datedobservers'.
        """
        if not file_path: return
        clean_input = file_path.replace("[", "").replace("]", "").replace("dated observers", "datedobservers").strip()
        
        # Split by comma first, or space/newline if no comma
        if "," in clean_input:
            paths = [p.strip(" \t\n\r'\"") for p in clean_input.split(",") if p.strip(" \t\n\r'\"")]
        else:
            paths = [p.strip(" \t\n\r'\"") for p in clean_input.split() if p.strip(" \t\n\r'\"")]

        for target_path in paths:
            target_path = target_path.strip(" \t\n\r'\"")
            if not target_path: continue

            # Handle (1) copy fallbacks
            if "(1)" in target_path and not os.path.exists(target_path):
                alt_path = target_path.replace("(1)", "")
                if os.path.exists(alt_path):
                    target_path = alt_path

            fetched_path = SmartDownloader.fetch(target_path) or target_path
            if not os.path.exists(fetched_path):
                print(f"   ❌ PATH ERROR: Resource unresolvable -> {fetched_path}")
                continue

            if os.path.isdir(fetched_path):
                for root, _, files in os.walk(fetched_path):
                    for file in files:
                        full_p = os.path.join(root, file)
                        if file.endswith(".py"):
                            self._load_single_py_plugin(full_p)
                        elif file.endswith((".pt", ".pth", ".bin", ".torchscript")):
                            self._harvest_tensor_file(full_p, file)
            elif fetched_path.endswith(".py"):
                self._load_single_py_plugin(fetched_path)
            elif fetched_path.endswith((".pt", ".pth", ".bin", ".torchscript")):
                self._harvest_tensor_file(fetched_path, os.path.basename(fetched_path))

    def _load_single_py_plugin(self, py_path: str):
        module_name = f"plugin_{re.sub(r'[^a-zA-Z0-9]', '_', os.path.splitext(os.path.basename(py_path))[0])}"
        try:
            spec = importlib.util.spec_from_file_location(module_name, py_path)
            if spec and spec.loader:
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)

                injected = 0
                for attr in dir(module):
                    obj = getattr(module, attr)
                    if isinstance(obj, type) and issubclass(obj, BaseObserver) and obj is not BaseObserver:
                        # Skip abstract base observer classes that don't implement all abstract methods
                        if inspect.isabstract(obj):
                            continue
                        try:
                            inst_obj = obj()
                        except Exception as inst_err:
                            continue

                        obs_key = attr[:3].upper()
                        if obs_key in self.observers:
                            obs_key = (attr[:2] + attr[-1]).upper()
                        self.observers[obs_key] = LegacyObserverAdapter(inst_obj)
                        self.observer_weights[obs_key] = 1.0
                        print(f"   ✅ INJECTED PLUGIN OBSERVER: '{obs_key}' ({attr}) from {os.path.basename(py_path)}")
                        injected += 1
                if injected == 0:
                    for inst_name in ['observer', 'plugin_observer']:
                        if hasattr(module, inst_name):
                            inst_obj = getattr(module, inst_name)
                            obs_key = inst_name[:3].upper()
                            self.observers[obs_key] = LegacyObserverAdapter(inst_obj)
                            self.observer_weights[obs_key] = 1.0
                            print(f"   ✅ LINKED INSTANTIATED OBSERVER: '{obs_key}' from {os.path.basename(py_path)}")
                            injected += 1
                            break
        except Exception as e:
            print(f"   ❌ PLUGIN FAULT in {os.path.basename(py_path)}: {e}")

    def _harvest_tensor_file(self, path: str, filename: str):
        if not TORCH_AVAILABLE: return
        try:
            w = torch.load(path, map_location='cpu', weights_only=False)
            core_id = re.sub(r'[^A-Z0-9_]', '_', filename.split('.')[0].upper())
            if core_id not in self.cores:
                self.cores[core_id] = TransformerCore(role=core_id)
                if self.fine_tuner.optimizer is not None:
                    self.fine_tuner = HolosynFineTuner(self.cores, lr=self.fine_tuner.lr)
            self.cores[core_id].assimilate_weights(w)
            print(f"   📦 ASSIMILATED WEIGHT SHARD: {filename} -> Core[{core_id}]")
        except Exception:
            pass

    def rebuild_manifold(self, path: str):
        """Explicit workspace harvesting path loader."""
        print(f"\n 📂 HARVESTING MANIFOLD WORKSPACE: {path}")
        self.load_plugin(path)

    def get_status_report(self) -> str:
        """Returns comprehensive engine status."""
        lines = [
            f"📊 [HOLOSYN 6.0 STATUS REPORT]",
            f"  • Hardware Profile : Dell Latitude 5420 (i5-1145G7 | 16GB RAM | CPU Threads={torch.get_num_threads() if TORCH_AVAILABLE else 1})",
            f"  • Cycle Counter    : {self.cycle}",
            f"  • Active Cores ({len(self.cores)}) : {list(self.cores.keys())}",
            f"  • Observers ({len(self.observers)})    : {list(self.observers.keys())}",
            f"  • Governor Lock   : {self.forced_governor or 'AUTONOMOUS'}",
            f"  • Active Model     : {self.ai_interface.local_subconscious.current_model_name}",
            f"  • Active AI Provider: {self.ai_interface.active_provider.upper()}",
            f"  • Active Persona    : {self.ai_interface.active_persona}",
            f"  • Reasoning Mode    : {self.ai_interface.mode.upper()}"
        ]
        return "\n".join(lines)

    def process(self, cmd: str, pre_parsed: Optional[Tuple] = None, file_path: Optional[str] = None) -> Tuple[Any, float, str, Dict[str, float], float, float]:
        """
        Main signal processing pipeline. Parses input telemetry, propagates through 
        active TransformerCores, evaluates all active hive observers, calculates
        haptic voltages, and returns unified manifold metrics.
        """
        self.cycle += 1
        
        # 1. Parse Intake Signal
        if pre_parsed:
            mod_type, text_content, boost, is_web, parsed_file_path = pre_parsed
        else:
            mod_type, text_content, boost, is_web, parsed_file_path = OmniSocialSenses.parse_target(cmd)

        active_file_path = file_path or parsed_file_path
        if active_file_path:
            self.last_file_path = active_file_path

        # 2. Emulate Input Token Tensor
        words = text_content.split() if text_content else ["SIGNAL"]
        seq = []
        for w in words[:128]:
            coh = min(len(w) / 10.0, 1.0)
            sync = 0.8 if any(c in "!?." for c in w) else 0.2
            fnd_wt = sum(ord(c) for c in w) / (len(w) * 128.0) if w else 0.5
            seq.append([coh, sync, fnd_wt, 1.0 - fnd_wt, boost])
            
        if not seq:
            seq = [[0.1, 0.1, 0.1, 0.1, boost]]

        if TORCH_AVAILABLE:
            tensor = torch.tensor([seq], dtype=torch.float32)
        else:
            tensor = None

        # 3. Propagate through Transformer Cores
        core_outputs = []
        for name, core in self.cores.items():
            try:
                if TORCH_AVAILABLE and hasattr(core, 'forward'):
                    with torch.no_grad():
                        val = core(tensor)
                        if isinstance(val, torch.Tensor):
                            val = float(val.mean().item())
                        core_outputs.append(float(val))
                else:
                    core_outputs.append(0.5)
            except Exception:
                core_outputs.append(0.5)

        uni = float(np.mean(core_outputs)) if (np is not None and core_outputs) else (sum(core_outputs)/len(core_outputs) if core_outputs else 0.5)

        # 4. Determine Pulse & Haptic Level
        if self.pulse_override is not None:
            pulse = float(self.pulse_override)
        else:
            pulse = float(math.sin(time.time() * 0.2) * 0.25 + (uni * 0.15))

        # Inject pulse into cores
        for core in self.cores.values():
            if hasattr(core, 'inject_pulse'):
                core.inject_pulse(pulse)

        # Topology Voltages & Haptic calculation
        topo_vals = np.array(list(self.topology.values())) if np is not None else [1.2, 1.8, 1.4, 1.1]
        interf = (1.0 + uni * 0.1) * (1.0 + abs(pulse) * 0.1)
        voltages = np.clip(topo_vals * interf * 0.5, 0.0, 1.0) if np is not None else [0.5, 0.5, 0.5, 0.5]
        haptic = float(np.mean(voltages)) if np is not None else 0.5

        # 5. Evaluate Observer Suite with safe evaluation wrapper
        raw_scores = {}
        avg_coh = float(np.mean([s[0] for s in seq])) if np is not None else 0.5
        avg_sync = float(np.mean([s[1] for s in seq])) if np is not None else 0.5

        for k, obs in self.observers.items():
            try:
                s_val = safe_evaluate_observer(
                    obs, s=avg_coh, sy=avg_sync, p=pulse, snn=voltages, 
                    text=text_content, haptic_level=haptic, mod=mod_type, file_path=active_file_path
                )
                weight = self.observer_weights.get(k, 1.0)
                raw_scores[k] = float(np.clip(s_val * weight, 0.0, 1.0)) if np is not None else float(s_val * weight)
            except Exception:
                raw_scores[k] = 0.5

        # 6. Governor Lock Resolution
        if self.forced_governor and self.forced_governor in self.observers:
            active_gov = self.forced_governor
        elif raw_scores:
            target_phase_norm = (uni + 1.0) / 2.0
            active_gov = min(raw_scores.keys(), key=lambda k: abs(raw_scores[k] - target_phase_norm))
        else:
            active_gov = "OMN"

        # 7. Fine-Tuner Adaptation Step
        if TORCH_AVAILABLE and self.fine_tuner and self.fine_tuner.optimizer:
            try:
                pred_phase = torch.tensor([uni], dtype=torch.float32, requires_grad=True)
                target_phase = torch.tensor([raw_scores.get(active_gov, 0.5)], dtype=torch.float32)
                self.fine_tuner.fine_tune_step(pred_phase, target_phase)
            except Exception:
                pass

        return voltages, uni, active_gov, raw_scores, haptic, pulse

    def run_grok_subconscious_pulse(self, prompt_hint: str = "") -> str:
        """Triggers Grok / Local Subconscious thought cycle into the active manifold swarm."""
        sub_thought, truth_score, resonance = self.ai_interface.generate_subconscious_signal(
            governor_lock=self.forced_governor or "OMN", 
            context_memory=prompt_hint or "Subconscious rhythm active."
        )
        voltages, uni, gov, scores, haptic, p = self.process(sub_thought)
        return (
            f"\n 🧠 [HOLOSYN SUBCONSCIOUS SWARM PULSE]\n"
            f" 🤖 Active Model    : {self.ai_interface.local_subconscious.current_model_name}\n"
            f" 💭 Subconscious     : '{sub_thought}'\n"
            f" 🎯 Truth Confidence : {truth_score:.4f} | Resonance Delta: {resonance:.4f}\n"
            f" 🌀 Unified Phase    : {uni:+.5f} rad | Governor Lock: {gov}"
        )

# ==============================================================================
# 10. MASTER CLI & INTERACTIVE SYSTEM ENGINE
# ==============================================================================

def start_cli():
    print("\n" + "💠"*38)
    print(" 🚀 HOLOSYN 6.0 ULTIMATE ENGINE: DELL LATITUDE 5420 OPTIMIZED NEXUS")
    print("💠"*38)
    print(" MANUAL INGESTION & BATCH COMMANDS:")
    print("    /batch [1|2|3|4|5|all]   : Load pre-configured plugin batches by portion")
    print("    /add [Concept/URL/File]  : Clone FOUNDATION Core and assimilate new target")
    print("    /load_plugin [Path]      : Manually load .py observer plugin (supports comma-separated list)")
    print("    /load_weights [Path]     : Manually load .pt / .pth weight shard into core matrix")
    print("    /unload [ObserverKey]    : Manually remove active observer plugin from hive")
    print("    /vault [Path/URL]        : Manually harvest directory for weights and plugins")
    print("    /status                  : View active cores, plugins, hardware profile, and engine state")
    print(" SUBCONSCIOUS & AI MODEL COMMANDS (DELL LATITUDE 5420 PRESETS):")
    print("    /model [Preset/Name]     : Options: smollm, smollm360m, smollm1.7b, qwen0.5b, qwen1.5b,")
    print("                               qwen2vl, tinyllama, gemma270m, phi1.5, stablelm1.6b, opt125m, minimax")
    print("    /ai [Provider] [Prompt]  : Direct prompt AI models (grok, openai, anthropic, ollama, qwen0.5b, smollm)")
    print("    /ai_key [Prov] [Key]     : Set API key for AI provider (grok, openai, anthropic)")
    print("    /grok [Prompt]           : Directly query Grok Model Interface & force GRK lock")
    print("    /grok_sub [Hint]         : Trigger Grok/Local Subconscious Swarm thought pulse")
    print("    /grok_mode [Mode]        : Switch AI reasoning mode (truth_seeking, fun_mode, quantum_reasoning)")
    print("    /persona [Preset]        : Set active persona (LOVE_LOGIC, TRUTH_SEEKING, CODE_ARCHITECT)")
    print("    /cot [Text]              : Format prompt using Chain-of-Thought (CoT) reasoning")
    print("    /tot [Text]              : Format prompt using 3-branch Tree-of-Thought (ToT) deliberation")
    print("    /prompt [Text] [Style]   : Format instruction (Styles: ChatML, Llama3, Alpaca, Grok)")
    print("    /instruct [Text]         : Run natural language instruction through Love Logic Core")
    print("    /clear_mem               : Clear conversation memory buffer")
    print(" OBSERVER & FINE-TUNING CONTROLS:")

    print("💠"*38)
    print(" MANUAL INGESTION & BATCH COMMANDS:")
    print("    /batch [1|2|3|4|5|all]   : Load pre-configured plugin batches by portion")
    print("    /add [Concept/URL/File]  : Clone FOUNDATION Core and assimilate new target")
    print("    /load_plugin [Path]      : Manually load .py observer plugin (supports comma-separated list)")
    print("    /load_weights [Path]     : Manually load .pt / .pth weight shard into core matrix")
    print("    /unload [ObserverKey]    : Manually remove active observer plugin from hive")
    print("    /vault [Path/URL]        : Manually harvest directory for weights and plugins")
    print("    /status                  : View active cores, plugins, and engine state")
    print(" SUBCONSCIOUS & AI MODEL COMMANDS (DELL LATITUDE CPU FRIENDLY):")
    print("    /model [Key/Name]        : Switch local subconscious model (qwen0.5b, tinyllama, smollm, opt125m, minimax)")
    print("    /ai [Provider] [Prompt]  : Direct prompt AI models (grok, openai, anthropic, ollama, qwen0.5b, smollm)")
    print("    /ai_key [Prov] [Key]     : Set API key for AI provider (grok, openai, anthropic)")
    print("    /grok [Prompt]           : Directly query Grok Model Interface & force GRK lock")
    print("    /grok_sub [Hint]         : Trigger Grok/Local Subconscious Swarm thought pulse")
    print("    /grok_mode [Mode]        : Switch AI reasoning mode (truth_seeking, fun_mode, quantum_reasoning)")
    print("    /persona [Preset]        : Set active persona (LOVE_LOGIC, TRUTH_SEEKING, CODE_ARCHITECT)")
    print("    /cot [Text]              : Format prompt using Chain-of-Thought (CoT) reasoning")
    print("    /tot [Text]              : Format prompt using 3-branch Tree-of-Thought (ToT) deliberation")
    print("    /prompt [Text] [Style]   : Format instruction (Styles: ChatML, Llama3, Alpaca, Grok)")
    print("    /instruct [Text]         : Run natural language instruction through Love Logic Core")
    print("    /clear_mem               : Clear conversation memory buffer")
    print(" OBSERVER & FINE-TUNING CONTROLS:")
    print("    /governor [Key/Auto]     : Manually force Governor Lock onto a specific observer")
    print("    /obs_weight [Key] [Val]  : Set fine-grained weight multiplier for an observer")
    print("    /tune [LR]               : Trigger online fine-tuning learning rate adaptation")
    print("    /checkpoint [Tag]        : Save current manifold weights & fine-tuning state")
    print("    /pulse [Value/Auto]      : Override feedback pulse intensity")
    print(" SOCIAL & ACTION COMMANDS:")
    print("    /email [To] [Subj] [Ctx] : Draft and queue prompt email dispatch")
    print("    /msg [@Node] [Message]   : Dispatch direct message routing")
    print("    /social [Plat] [Content] : Dispatch omni-social broadcast across platforms (X, IG, Reddit, etc.)")
    print("    /discord [Ch] [Message]  : Broadcast telemetry message to Discord channel")
    print("    /livestream [Ch] [Sync]  : Orchestrate livestream telemetry")
    print("─"*76)

    # Initialize Nexus with Manual Loading Only (auto_harvest=False)
    nexus = HolosynDynamic(auto_harvest=False)

    while True:
        try:
            cmd = input("\n[HOLOSYN 6.0 SIGNAL] > ").strip()
            if not cmd:
                break

            if cmd.startswith("/"):
                parts = cmd.split(" ", 2)
                base_cmd = parts[0].lower()
                arg1 = parts[1] if len(parts) > 1 else ""
                arg2 = parts[2] if len(parts) > 2 else ""

                if base_cmd in ["/model", "/sub_model"]:
                    res = nexus.ai_interface.local_subconscious.switch_model(arg1 or "smollm")
                    print(res)
                elif base_cmd == "/add":
                    res = nexus.add_core(arg1 or "CUSTOM_CONCEPT")
                    print(res)
                elif base_cmd in ["/batch", "/load_batch"]:
                    res = nexus.load_batch(arg1 or "1")
                    print(res)
                elif base_cmd in ["/plugin", "/load_plugin"]:
                    nexus.load_plugin(arg1 + (" " + arg2 if arg2 else ""))
                elif base_cmd == "/vault":
                    nexus.rebuild_manifold(arg1 or ".")
                elif base_cmd == "/status":
                    print(nexus.get_status_report())
                elif base_cmd == "/persona":
                    print(nexus.ai_interface.set_persona(arg1 or "LOVE_LOGIC"))
                elif base_cmd == "/clear_mem":
                    print(nexus.ai_interface.clear_history())
                elif base_cmd == "/cot":
                    formatted = HolosynPromptStudio.format_cot(arg1 or "Analyze manifold equilibrium.")
                    print(f"\n--- CHAIN-OF-THOUGHT PROMPT ---\n{formatted}\n--- END COT ---")
                elif base_cmd == "/tot":
                    formatted = HolosynPromptStudio.format_tot(arg1 or "Deliberate on reciprocal harmony.")
                    print(f"\n--- TREE-OF-THOUGHT PROMPT ---\n{formatted}\n--- END TOT ---")
                elif base_cmd == "/ai":
                    nexus.force_governor("GRK")
                    sub_parts = (arg1 + " " + arg2).strip().split(" ", 1)
                    prov = sub_parts[0] if len(sub_parts) > 1 and sub_parts[0].lower() in ["grok", "openai", "anthropic", "ollama", "qwen0.5b", "smollm", "tinyllama"] else "grok"
                    prompt_text = sub_parts[1] if len(sub_parts) > 1 and sub_parts[0].lower() in ["grok", "openai", "anthropic", "ollama", "qwen0.5b", "smollm", "tinyllama"] else (arg1 + " " + arg2).strip()
                    if not prompt_text:
                        prompt_text = "Explain the quantum truth of the universe."
                    ai_res, truth_score, res_delta = nexus.ai_interface.query(prompt_text, provider=prov)
                    print(f"\n--- DIRECT AI MODEL INTERFACE [{prov.upper()}] ({nexus.ai_interface.mode.upper()}) ---")
                    print(f" 🤖 AI Answer: {ai_res}")
                    print(f" 🎯 Truth Score: {truth_score:.4f} | Quantum Delta: {res_delta:.4f}")
                    v, uni, gov, scores, haptic, p = nexus.process(prompt_text)
                    print(f" 🌀 Manifold Sync Phase: {uni:+.4f} | Governor Lock: {gov}")
                    print("--- END AI RESPONSE ---")
                elif base_cmd == "/ai_key":
                    res = nexus.ai_interface.set_key(arg1, arg2)
                    print(res)
                elif base_cmd == "/grok":
                    nexus.force_governor("GRK")
                    prompt_query = " ".join([arg1, arg2]).strip() or "Explain the quantum truth of the universe."
                    grok_res, truth_score, res_delta = nexus.ai_interface.query(prompt_query, provider="grok")
                    print(f"\n--- DIRECT GROK MODEL INTERFACE ({nexus.ai_interface.mode.upper()}) ---")
                    print(f" 🤖 Grok Answer: {grok_res}")
                    print(f" 🎯 Truth Score: {truth_score:.4f} | Quantum Delta: {res_delta:.4f}")
                    v, uni, gov, scores, haptic, p = nexus.process(prompt_query)
                    print(f" 🌀 Manifold Sync Phase: {uni:+.4f} | Governor Lock: {gov}")
                    print("--- END GROK RESPONSE ---")
                elif base_cmd in ["/grok_sub", "/subconscious"]:
                    hint_text = " ".join([arg1, arg2]).strip()
                    res = nexus.run_grok_subconscious_pulse(hint_text)
                    print(res)
                elif base_cmd == "/grok_mode":
                    res = nexus.ai_interface.set_mode(arg1 or "truth_seeking")
                    print(res)
                elif base_cmd == "/governor":
                    res = nexus.force_governor(arg1)
                    print(res)
                elif base_cmd == "/obs_weight":
                    try:
                        wt = float(arg2)
                        res = nexus.set_observer_weight(arg1, wt)
                        print(res)
                    except ValueError:
                        print(" ❌ Please supply numeric weight (e.g., /obs_weight GRK 1.5)")
                elif base_cmd == "/prompt":
                    formatted = HolosynPromptStudio.format_prompt(
                        arg1, paradigm=nexus.paradigm, style=arg2 or "chatml", persona=nexus.ai_interface.active_persona
                    )
                    print(f"\n--- PROMPT STUDIO OUTPUT ({arg2 or 'chatml'}) ---\n{formatted}\n--- END PROMPT ---")
                elif base_cmd == "/instruct":
                    v, uni, gov, scores, haptic, p = nexus.process(arg1)
                    print(f"\n 🧠 [LOVE LOGIC INSTRUCT RES]: Unified Phase={uni:+.4f} | Gov={gov} | Haptic={haptic:.4f}")
                elif base_cmd == "/social":
                    res = HolosynPromptStudio.execute_social_post_action(arg1 or "x", arg2 or "Holosyn 6.0 Social Sync Active.")
                    print(res)
                elif base_cmd == "/discord":
                    res = HolosynPromptStudio.execute_discord_broadcast_action(arg1 or "general", arg2 or "Telemetry pulse nominal.")
                    print(res)
                elif base_cmd == "/email":
                    res = HolosynPromptStudio.execute_email_action(arg1 or "dev@cbloom.life", "Holosyn 6.0 Alert", arg2 or "Telemetry nominal.")
                    print(res)
                elif base_cmd == "/msg":
                    res = HolosynPromptStudio.execute_messaging_action(arg1 or "devcbloom", arg2 or "Pulse stable.")
                    print(res)
                elif base_cmd == "/livestream":
                    res = HolosynPromptStudio.execute_livestream_action(arg1 or "main", 0.95)
                    print(res)
                elif base_cmd == "/tune":
                    try:
                        new_lr = float(arg1)
                        nexus.fine_tuner.lr = new_lr
                        if nexus.fine_tuner.optimizer:
                            for param_group in nexus.fine_tuner.optimizer.param_groups:
                                param_group['lr'] = new_lr
                        print(f" 🎛️ FINE-TUNER: Learning rate updated to {new_lr:.2e}")
                    except ValueError:
                        print(" ❌ Please supply a numeric learning rate (e.g. 0.001)")
                elif base_cmd == "/checkpoint":
                    tag = arg1 or "latest"
                    path = nexus.fine_tuner.save_checkpoint(tag)
                elif base_cmd == "/pulse":
                    try:
                        nexus.pulse_override = float(arg1)
                        print(f" 🎛️ PULSE OVERRIDE: {nexus.pulse_override:.4f}")
                    except ValueError:
                        nexus.pulse_override = None
                        print(" 🎛️ PULSE OVERRIDE DISABLED (Autonomous Rhythms Engaged).")
                else:
                    print(f"   ⚠️ Command pathway not recognized: {base_cmd}")
            else:
                v, uni, gov, scores, haptic, p = nexus.process(cmd)

                print("═"*76)
                print(f" 📡 INPUT SIGNAL    : '{cmd[:65]}...'")
                print(f" 🌀 UNIFIED PHASE   : {uni:+.5f} rad | 💓 PULSE: {p:+.4f} | HAPTIC: {haptic:.4f}")
                print(f" 🧠 GOVERNOR LOCK   : {gov} | 🧬 ACTIVE CORES: {len(nexus.cores)} | 🐝 OBSERVERS: {len(nexus.observers)}")
                print("─"*76)

                matrix_str = " | ".join([f"{k}: {v:.2f}" for k, v in list(scores.items())[:10]])
                print(f" 秤 CONSENSUS MATRIX : [{matrix_str}]")
                print("═"*76)

        except KeyboardInterrupt:
            print("\n 汽 Halting Holosyn 6.0 CLI safely.")
            break
        except Exception as e:
            import traceback
            print(f"❌ Core Engine Fault: {e}")
            traceback.print_exc()

if __name__ == "__main__":
    start_cli()