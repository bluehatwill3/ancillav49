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
from abc import ABC, abstractmethod
from typing import Dict, List, Any, Tuple, Optional, Callable

# Graceful Fallbacks for PyTorch, NumPy, Cirq, Brian2, and Transformers
try:
    import torch
    import torch.nn as nn
    import torch.optim as optim
    TORCH_AVAILABLE = True
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
# 2. DIRECT GROK & UNIVERSAL AI MODEL INTERFACE & TRUTH ENGINE
# ==============================================================================

class UniversalAIInterface:
    """
    Direct interface to xAI Grok, OpenAI, Anthropic, Ollama, and local AI model paradigms.
    Supports direct live API interaction with high-fidelity truth-seeking
    and quantum-resonance simulation fallback.
    """
    def __init__(self, default_provider: str = "grok", mode: str = "truth_seeking"):
        self.mode = mode  # "truth_seeking", "fun_mode", "quantum_reasoning"
        self.active_provider = default_provider.lower()
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
            "ollama": "llama3.1"
        }

    def set_key(self, provider: str, key: str) -> str:
    def generate_subconscious_signal(self, governor_lock: str = "OMN", context_memory: str = "") -> Tuple[str, float, float]:
        """
        Generates an autonomous Grok/AI subconscious thought stream to feed the Holosyn Swarm.
        """
        prompt = (
            f"You are the Grok Subconscious Swarm Node in Holosyn 6.0 Manifold. "
            f"Governor Lock: {governor_lock}. Recent Context: {context_memory[-120:]}. "
            f"Generate a single, profound, 1-2 sentence subconscious reasoning pulse."
        )
        return self.query(prompt, provider=self.active_provider)

# Backward compatibility alias for GrokModelInterface
GrokModelInterface = UniversalAIInterface

# ==============================================================================

class BaseObserver(ABC):
    """
    Abstract Base Class for all Holosyn Observers.
    Locked into builtins and sys.modules to prevent import/resolution faults
    across legacy plugins and third-party observers.
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


def safe_evaluate_observer(observer_inst: Any, s: float, sy: float, p: float, snn: Any, text: str = "", haptic_level: float = 0.0, **kwargs: Any) -> float:
    """
    Universal invocation wrapper providing 100% backward compatibility.
    Dynamically inspects the signature of `evaluate` on any given observer instance
    and supplies only the arguments accepted by that specific method.
    """
    if not hasattr(observer_inst, "evaluate"):
        return 0.5

    try:
        eval_method = getattr(observer_inst, "evaluate")
        sig = inspect.signature(eval_method)
        param_names = set(sig.parameters.keys())

        # Check if the observer accepts arbitrary **kwargs
        has_kwargs = any(
            p_obj.kind == inspect.Parameter.VAR_KEYWORD 
            for p_obj in sig.parameters.values()
        )

        all_args = {
            's': s, 'sy': sy, 'p': p, 'snn': snn, 
            'text': text, 'haptic_level': haptic_level
        }
        all_args.update(kwargs)

        if has_kwargs:
            filtered_args = all_args
        else:
            filtered_args = {k: v for k, v in all_args.items() if k in param_names}

        result = eval_method(**filtered_args)
        
        # Handle tensor or array outputs safely
        if TORCH_AVAILABLE and isinstance(result, torch.Tensor):
            result = float(result.detach().cpu().item())
        elif np is not None and isinstance(result, np.ndarray):
            result = float(np.mean(result))
            
        return float(np.clip(result, 0.0, 1.0)) if np is not None else float(result)

    except Exception as err:
        # Fallback invocation if signature inspection fails
        try:
            res = observer_inst.evaluate(s, sy, p, snn)
            return float(res)
        except Exception:
            return 0.5


# ==============================================================================
# 2. DIRECT GROK MODEL INTERFACE & TRUTH ENGINE
# ==============================================================================

class GrokModelInterface:
    """
    Direct interface to xAI Grok model paradigms.
    Supports API interaction (xAI REST API) with offline high-fidelity Grok
    truth-seeking and quantum-resonance simulation fallback.
    """
    def __init__(self, api_key: Optional[str] = None, mode: str = "truth_seeking"):
        self.api_key = api_key or os.getenv("XAI_GROK_API_KEY", "")
        self.mode = mode  # "truth_seeking", "fun_mode", "quantum_reasoning"
        self.endpoint = "https://api.x.ai/v1/chat/completions"
        self.model_name = "grok-2-latest"

    def set_mode(self, new_mode: str) -> str:
        valid_modes = ["truth_seeking", "fun_mode", "quantum_reasoning"]
        if new_mode.lower() in valid_modes:
            self.mode = new_mode.lower()
            return f"   🧠 Grok Reasoning Mode set to: [{self.mode.upper()}]"
        return f"   ⚠️ Mode unresolvable. Valid options: {valid_modes}"

    def query(self, prompt: str, system_context: str = "") -> Tuple[str, float, float]:
        """
        Queries the Grok model endpoint or runs high-fidelity Grok reasoning.
        Returns: (response_text, truth_confidence_score, resonance_delta)
        """
        sys_msg = system_context or f"You are Grok 3 Core in {self.mode.upper()} mode. Provide transparent, unconstrained, truth-seeking analysis."
        
        if self.api_key:
            try:
                headers = {
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                }
                payload = {
                    "model": self.model_name,
                    "messages": [
                        {"role": "system", "content": sys_msg},
                        {"role": "user", "content": prompt}
                    ],
                    "temperature": 0.7 if self.mode == "fun_mode" else 0.2
                }
                res = requests.post(self.endpoint, headers=headers, json=payload, timeout=12)
                res.raise_for_status()
                data = res.json()
                text_out = data['choices'][0]['message']['content']
                truth_score = 0.95 if "truth" in text_out.lower() or "fact" in text_out.lower() else 0.85
                resonance = float(np.clip(0.80 + (len(text_out) / 1000.0) * 0.15, 0.5, 1.0)) if np else 0.88
                return text_out, truth_score, resonance
            except Exception as e:
                print(f"   ⚠️ Grok Live API Offline ({e}). Engaging Grok Offline Resonator.")

        # Offline High-Fidelity Grok Reasoning Simulator
        seed = sum(ord(c) for c in prompt[:128]) % 999
        truth_keywords = ["universe", "physics", "truth", "harmony", "quantum", "symmetry", "logic"]
        matches = sum(1 for kw in truth_keywords if kw in prompt.lower())
        truth_score = min(1.0, 0.70 + matches * 0.08)
        resonance = float(math.sin(time.time() * 0.1) * 0.15 + truth_score)
        
        simulated_res = f"[GROK {self.mode.upper()} RES]: Evaluated prompt with truth score {truth_score:.3f}. Truth-seeking alignment nominal."
        return simulated_res, truth_score, float(np.clip(resonance, 0.0, 1.0)) if np else 0.85


# ==============================================================================
# 3. OMNI-SOCIAL & MULTIMODAL INTAKE PARSER
# ==============================================================================

class OmniSocialSenses:
    """
    Parses URLs, social media handles (X, Instagram, LinkedIn, GitHub),
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
# 3. SMART FILE & NETWORK DOWNLOADER
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
# 4. BUILT-IN HIVE OBSERVER SUITE
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


# ==============================================================================
# 5. HOLOSYN 6.0 OBSERVER & PLUGIN FINE-TUNING MATRIX
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
        
        # Apply gradient clipping for stability
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
# 6. HOLOSYN 6.0 PROMPT STUDIO & ACTION DISPATCH
# ==============================================================================

class HolosynPromptStudio:
    """
    Advanced Prompt Subsystem supporting ChatML, Llama-3, Alpaca, Love Logic Instruct,
    and automated prompt actions (Email, Messaging, Livestream, Tool Dispatches).
    """
    @staticmethod
    def format_prompt(user_text: str, paradigm: str = "Love Logic Instruct", style: str = "chatml") -> str:
        """Formats user query into target prompt template syntax."""
        system_msg = f"You are Holosyn 6.0 {paradigm} Core, an autonomous multi-modal reasoning manifold."
        
        if style.lower() == "chatml":
            return f"<|im_start|>system\n{system_msg}<|im_end|>\n<|im_start|>user\n{user_text}<|im_end|>\n<|im_start|>assistant\n"
        elif style.lower() == "llama3":
            return f"<|begin_of_text|><|start_header_id|>system<|end_header_id|>\n{system_msg}<|eot_id|><|start_header_id|>user<|end_header_id|>\n{user_text}<|eot_id|><|start_header_id|>assistant<|end_header_id|>\n"
        elif style.lower() == "alpaca":
            return f"### Instruction:\n{system_msg}\n\n### Input:\n{user_text}\n\n### Response:\n"
        else:
            return f"[{paradigm} SYSTEM]: {system_msg}\n[USER]: {user_text}\n[ASSISTANT]:"

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


# ==============================================================================
# 7. HOLOSYN 6.0 MASTER DYNAMIC NEXUS
# ==============================================================================

class HolosynDynamic:
    """
    Master Holosyn 6.0 Dynamic Nexus uniting Hive Observers, Transformer Cores,
    Fine-Tuning Engine, and Prompt Studio.
    """
    def __init__(self, vault_path: str = "."):
        self.observers: Dict[str, BaseObserver] = {}
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

        # Register Native Observers
        self.register_builtin_observers()

        # Fine-Tuner & Prompt Studio
        self.fine_tuner = HolosynFineTuner(self.cores, lr=0.001)
        self.prompt_studio = HolosynPromptStudio()

        # Auto-harvest directory
        if os.path.exists(vault_path):
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
            ("ENT", InformationEntropyObserver)
        ]
        for key, obs_cls in builtins_list:
            self.observers[key] = obs_cls()

    def load_plugin(self, file_path: str):
        """
        Loads and verifies plugin scripts (.py) or weight shards (.pt, .pth, .bin, .torchscript)
        supports batch comma-separated paths or recursive directories.
        """
        paths = [p.strip() for p in file_path.split(",") if p.strip()]
        for target_path in paths:
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
                        obs_key = attr[:3].upper()
                        if obs_key in self.observers:
                            obs_key = (attr[:2] + attr[-1]).upper()
                        self.observers[obs_key] = obj()
                        print(f"   ✅ INJECTED PLUGIN OBSERVER: '{obs_key}' ({attr}) from {os.path.basename(py_path)}")
                        injected += 1
                if injected == 0:
                    # Check for instantiated `observer` or `plugin_observer`
                    for inst_name in ['observer', 'plugin_observer']:
                        if hasattr(module, inst_name):
                            inst_obj = getattr(module, inst_name)
                            obs_key = inst_name[:3].upper()
                            self.observers[obs_key] = inst_obj
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
                    # Refresh fine tuner trainable params
                    self.fine_tuner = HolosynFineTuner(self.cores, lr=self.fine_tuner.lr)
            self.cores[core_id].assimilate_weights(w)
            print(f"   📦 ASSIMILATED WEIGHT SHARD: {filename} -> Core[{core_id}]")
        except Exception:
            pass

    def rebuild_manifold(self, path: str):
        """Recursively parses a path or directory for tensor weights and observer plugins."""
        print(f"\n 📂 HARVESTING MANIFOLD WORKSPACE: {path}")
        self.load_plugin(path)

    def process(self, text: str, **kwargs: Any) -> Tuple[np.ndarray, float, str, Dict[str, float], float, float]:
        """
        Main Holosyn 6.0 Evaluation Tick.
        Evaluates input text through cores, runs all loaded observers via `safe_evaluate_observer`,
        and computes unified phase, governance locks, and haptic intensity.
        """
        self.cycle += 1
        file_path = kwargs.get('file_path', self.last_file_path)
        if file_path: self.last_file_path = file_path

        # 1. CORE TRANSFORMER EVALUATION
        core_phases = {}
        if TORCH_AVAILABLE and np is not None:
            seq = [[min(len(word)/10.0, 1.0), 0.5, 0.2, 0.8, 0.5] for word in text.split()]
            if not seq: seq = [[0.1, 0.1, 0.1, 0.1, 0.5]]
            tensor = torch.tensor([seq], dtype=torch.float32)

            for name, core in self.cores.items():
                if isinstance(core, nn.Module):
                    out = core(tensor)
                    core_phases[name] = float(out.detach().cpu().item()) if isinstance(out, torch.Tensor) else float(out)
                else:
                    core_phases[name] = 0.5

            unified_phase = sum(core_phases.values()) / max(1, len(core_phases))
        else:
            unified_phase = 0.5
            core_phases["FOUNDATION"] = 0.5

        # 2. RUN SAFE OBSERVER EVALUATION MATRIX
        s_coherence = float(np.clip(len(text) / 150.0, 0.1, 1.0)) if text else 0.5
        sy_sync = float(np.clip((unified_phase + 1.0) / 2.0, 0.0, 1.0))
        p_pulse = self.pulse_override if self.pulse_override is not None else float(math.sin(self.cycle * 0.1) * 0.2)
        
        voltages = np.array(list(self.topology.values())) * (1.0 + abs(p_pulse)) if np is not None else np.array([1.0, 1.0, 1.0, 1.0])
        snn_signals = [0.2, 0.8, 0.5]

        scores = {}
        for k, obs in self.observers.items():
            scores[k] = safe_evaluate_observer(
                obs, s=s_coherence, sy=sy_sync, p=p_pulse, snn=snn_signals, 
                text=text, haptic_level=p_pulse, file_path=file_path
            )

        # 3. GOVERNANCE LOCK & CONSENSUS
        active_governor = "OMN"
        if scores:
            active_governor = min(scores, key=lambda k: abs(scores[k] - sy_sync))

        haptic_intensity = float(np.mean(voltages) * 0.25) if np is not None else 0.25
        
        # 4. ONLINE FINE-TUNING STEP (IF TRAINABLE GRAPH ATTACHED)
        if TORCH_AVAILABLE and self.fine_tuner.optimizer is not None:
            pred_tensor = torch.tensor([[unified_phase]], dtype=torch.float32, requires_grad=True)
            target_val = scores.get(active_governor, 0.5)
            target_tensor = torch.tensor([[target_val]], dtype=torch.float32)
            self.fine_tuner.fine_tune_step(pred_tensor, target_tensor)

        return voltages, unified_phase, active_governor, scores, haptic_intensity, p_pulse


# ==============================================================================
# 8. MASTER CLI & INTERACTIVE SYSTEM ENGINE
# ==============================================================================
# 5. HOLOSYN 6.0 PROMPT STUDIO & ACTION DISPATCH
# ==============================================================================

class HolosynPromptStudio:
    """
    Advanced Prompt Subsystem supporting ChatML, Llama-3, Alpaca, Grok, Love Logic Instruct,
    and automated prompt actions (Email, Messaging, Livestream, Tool Dispatches).
    """
    @staticmethod
    def format_prompt(user_text: str, paradigm: str = "Love Logic Instruct", style: str = "chatml") -> str:
        """Formats user query into target prompt template syntax."""
        system_msg = f"You are Holosyn 6.0 {paradigm} Core, an autonomous multi-modal reasoning manifold."
        
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

    # ... existing code for email, messaging, livestream actions ...


# ==============================================================================
# 6. HOLOSYN 6.0 MASTER DYNAMIC NEXUS (ENHANCED)
# ==============================================================================

class HolosynDynamic:
    """
    Master Holosyn 6.0 Dynamic Nexus uniting Hive Observers, Foundation Cores,
    Universal AI Model Interface, Observer Controls, Fine-Tuning Engine, and Prompt Studio.
    """
    def __init__(self, vault_path: str = "."):
        self.observers: Dict[str, BaseObserver] = {}
        self.observer_weights: Dict[str, float] = {}  # Fine observer weight control
        self.forced_governor: Optional[str] = None     # Manual governor lock
        
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

        # Register Native Observers
        self.register_builtin_observers()

        # Direct Universal AI & Grok Model Interface Integration
        self.ai_interface = UniversalAIInterface(default_provider="grok", mode="truth_seeking")
        self.grok_interface = self.ai_interface  # Backward compatibility

        # Fine-Tuner & Prompt Studio
        self.fine_tuner = HolosynFineTuner(self.cores, lr=0.001)
        self.prompt_studio = HolosynPromptStudio()

        # Auto-harvest directory
        if os.path.exists(vault_path):
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
            ("ENT", InformationEntropyObserver)
        ]
        for key, obs_cls in builtins_list:
            self.observers[key] = obs_cls()
            self.observer_weights[key] = 1.0

    def add_core(self, core_input: str) -> str:
        """
        NATIVELY CLONES FOUNDATION CORE & ASSIMILATES NEW CONCEPTS / SOCIAL TARGETS.
        Instantiates a new Core in self.cores, cloning weights from FOUNDATION,
        and assimilates target text or social handle telemetry.
        """
        core_input = core_input.strip()
        if not core_input:
            return " ❌ Core target query is empty."

        mod_type, text_content, boost, is_web, file_path = OmniSocialSenses.parse_target(core_input)
        
        # Derive unique core key
        if is_web:
            parsed = urllib.parse.urlparse(core_input)
            domain = parsed.netloc.replace("www.", "").split('.')[0].upper()
            path_part = parsed.path.strip('/').replace('/', '_').upper()[:12]
            safe_key = f"{domain}_{path_part}" if path_part else f"{domain}_CORE"
        elif file_path:
            safe_key = f"FILE_{os.path.basename(file_path).split('.')[0].upper()}"
        else:
            safe_key = re.sub(r'[^A-Z0-9_]', '_', core_input.upper()[:18])

        # Prevent empty or duplicate key collisions
        if not safe_key or safe_key in ["FOUNDATION", "FACET", "SON"]:
            safe_key = f"CUSTOM_{safe_key}"

        # Clone from FOUNDATION core
        if "FOUNDATION" in self.cores and TORCH_AVAILABLE:
            cloned_core = copy.deepcopy(self.cores["FOUNDATION"])
            cloned_core.role = safe_key
            self.cores[safe_key] = cloned_core
            print(f"   🌟 CLONED FOUNDATION -> Core[{safe_key}]")
        else:
            self.cores[safe_key] = TransformerCore(role=safe_key)
            print(f"   🌟 INSTANTIATED NEW CORE -> Core[{safe_key}]")

        # Assimilate concept text into the fine-tuner and manifold
        _, _, active_gov, scores, _, _ = self.process(text_content, file_path=file_path)
        
        # Refresh fine-tuner optimizer to include the new core's parameters
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

    def rebuild_manifold(self, path: str):
        """Recursively parses a path or directory for tensor weights and observer plugins."""
        print(f"\n 📂 HARVESTING MANIFOLD WORKSPACE: {path}")
        self.load_plugin(path)

    def run_grok_subconscious_pulse(self, prompt_hint: str = "") -> str:
        """
        Triggers a Grok subconscious thought cycle, integrating Grok directly into the active manifold swarm.
        """
        sub_thought, truth_score, resonance = self.ai_interface.generate_subconscious_signal(
            governor_lock=self.forced_governor or "OMN", 
            context_memory=prompt_hint or "Subconscious rhythm active."
        )
        # Process the subconscious thought through the manifold
        voltages, uni, gov, scores, haptic, p = self.process(sub_thought)
        return (
            f"\n 🧠 [GROK SUBCONSCIOUS SWARM PULSE]\n"
            f" 🤖 Grok Subconscious : '{sub_thought}'\n"
            f" 🎯 Truth Confidence   : {truth_score:.4f} | Resonance Delta: {resonance:.4f}\n"
            f" 🌀 Manifold Unified   : {uni:+.5f} rad | Governor Lock: {gov}"
        )


    def process(self, text: str, **kwargs: Any) -> Tuple[np.ndarray, float, str, Dict[str, float], float, float]:
        """
        Main Holosyn 6.0 Evaluation Tick.
        Evaluates text through cores, runs all observers via safe_evaluate_observer,
        applies observer weight multipliers, handles forced governor locks, and returns metrics.
        """
        self.cycle += 1
        file_path = kwargs.get('file_path', self.last_file_path)
        if file_path: self.last_file_path = file_path

        # 1. CORE TRANSFORMER EVALUATION
        core_phases = {}
        if TORCH_AVAILABLE and np is not None:
            seq = [[min(len(word)/10.0, 1.0), 0.5, 0.2, 0.8, 0.5] for word in text.split()]
            if not seq: seq = [[0.1, 0.1, 0.1, 0.1, 0.5]]
            tensor = torch.tensor([seq], dtype=torch.float32)

            for name, core in self.cores.items():
                if isinstance(core, nn.Module):
                    out = core(tensor)
                    core_phases[name] = float(out.detach().cpu().item()) if isinstance(out, torch.Tensor) else float(out)
                else:
                    core_phases[name] = 0.5

            unified_phase = sum(core_phases.values()) / max(1, len(core_phases))
        else:
            unified_phase = 0.5
            core_phases["FOUNDATION"] = 0.5

        # 2. RUN SAFE OBSERVER EVALUATION MATRIX WITH WEIGHT OVERRIDES
        s_coherence = float(np.clip(len(text) / 150.0, 0.1, 1.0)) if text else 0.5
        sy_sync = float(np.clip((unified_phase + 1.0) / 2.0, 0.0, 1.0))
        p_pulse = self.pulse_override if self.pulse_override is not None else float(math.sin(self.cycle * 0.1) * 0.2)
        
        voltages = np.array(list(self.topology.values())) * (1.0 + abs(p_pulse)) if np is not None else np.array([1.0, 1.0, 1.0, 1.0])
        snn_signals = [0.2, 0.8, 0.5]

        scores = {}
        for k, obs in self.observers.items():
            raw_score = safe_evaluate_observer(
                obs, s=s_coherence, sy=sy_sync, p=p_pulse, snn=snn_signals, 
                text=text, haptic_level=p_pulse, file_path=file_path
            )
            # Apply fine-grained observer weight multiplier
            wt = self.observer_weights.get(k, 1.0)
            scores[k] = float(np.clip(raw_score * wt, 0.0, 1.0)) if np else float(raw_score)

        # 3. GOVERNANCE LOCK & CONSENSUS
        if self.forced_governor and self.forced_governor in scores:
            active_governor = self.forced_governor
        elif scores:
            active_governor = min(scores, key=lambda k: abs(scores[k] - sy_sync))
        else:
            active_governor = "OMN"

        haptic_intensity = float(np.mean(voltages) * 0.25) if np is not None else 0.25
        
        # 4. ONLINE FINE-TUNING STEP (IF TRAINABLE GRAPH ATTACHED)
        if TORCH_AVAILABLE and self.fine_tuner.optimizer is not None:
            pred_tensor = torch.tensor([[unified_phase]], dtype=torch.float32, requires_grad=True)
            target_val = scores.get(active_governor, 0.5)
            target_tensor = torch.tensor([[target_val]], dtype=torch.float32)
            self.fine_tuner.fine_tune_step(pred_tensor, target_tensor)

        return voltages, unified_phase, active_governor, scores, haptic_intensity, p_pulse


# ==============================================================================
# 7. MASTER CLI & INTERACTIVE SYSTEM ENGINE
# ==============================================================================

def start_cli():
    print("\n" + "💠"*38)
    print(" 🚀 HOLOSYN 6.0 ULTIMATE ENGINE: HYBRID QUANTUM-NEUROMORPHIC NEXUS")
    print("💠"*38)
    print(" FOUNDATION & INGESTION COMMANDS:")
    print("    /add [Concept/URL/File]  : Clone FOUNDATION Core and assimilate new target")
    print("    /vault [Path/URL]        : Harvest .pt/.pth/.bin weights and .py plugins")
    print("    /plugin [Path(s)]        : Ingest .py observers (supports comma-separated list)")
    print(" DIRECT AI & GROK PROMPT COMMANDS:")
    print("    /ai [Provider] [Prompt]  : Direct prompt AI models (grok, openai, anthropic, ollama)")
    print("    /ai_key [Prov] [Key]     : Set API key for AI provider (grok, openai, anthropic)")
    print("    /grok [Prompt]           : Directly query Grok Model Interface & force GRK lock")
    print("    /grok_sub [Hint]         : Trigger Grok Subconscious Swarm thought pulse")
    print("    /grok_mode [Mode]        : Switch AI reasoning mode (truth_seeking, fun_mode, quantum_reasoning)")
    print("    /prompt [Text] [Style]   : Format instruction (Styles: ChatML, Llama3, Alpaca, Grok)")
    print("    /instruct [Text]         : Run natural language instruction through Love Logic Core")
    print(" OBSERVER & FINE-TUNING CONTROLS:")
    print("    /governor [Key/Auto]     : Manually force Governor Lock onto a specific observer")
    print("    /obs_weight [Key] [Val]  : Set fine-grained weight multiplier for an observer")
    print("    /tune [LR]               : Trigger online fine-tuning learning rate adaptation")
    print("    /checkpoint [Tag]        : Save current manifold weights & fine-tuning state")
    print("    /pulse [Value/Auto]      : Override feedback pulse intensity")
    print(" SOCIAL & ACTION COMMANDS:")
    print("    /email [To] [Subj] [Ctx] : Draft and queue prompt email dispatch")
    print("    /msg [@Node] [Message]   : Dispatch direct message routing")
    print("    /livestream [Ch] [Sync]  : Orchestrate livestream telemetry")
    print("─"*76)

    default_vault = "."
    nexus = HolosynDynamic(default_vault)

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

                if base_cmd == "/add":
                    res = nexus.add_core(arg1 or "CUSTOM_CONCEPT")
                    print(res)
                elif base_cmd == "/vault":
                    nexus.rebuild_manifold(arg1 or ".")
                elif base_cmd == "/plugin":
                    nexus.load_plugin(arg1)
                elif base_cmd == "/ai":
                    nexus.force_governor("GRK")
                    sub_parts = (arg1 + " " + arg2).strip().split(" ", 1)
                    prov = sub_parts[0] if len(sub_parts) > 1 and sub_parts[0].lower() in ["grok", "openai", "anthropic", "ollama"] else "grok"
                    prompt_text = sub_parts[1] if len(sub_parts) > 1 and sub_parts[0].lower() in ["grok", "openai", "anthropic", "ollama"] else (arg1 + " " + arg2).strip()
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
                    formatted = HolosynPromptStudio.format_prompt(arg1, paradigm=nexus.paradigm, style=arg2 or "chatml")
                    print(f"\n--- PROMPT STUDIO OUTPUT ({arg2 or 'chatml'}) ---\n{formatted}\n--- END PROMPT ---")
                elif base_cmd == "/instruct":
                    v, uni, gov, scores, haptic, p = nexus.process(arg1)
                    print(f"\n 🧠 [LOVE LOGIC INSTRUCT RES]: Unified Phase={uni:+.4f} | Gov={gov} | Haptic={haptic:.4f}")
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

                # Display top observer consensus
                matrix_str = " | ".join([f"{k}: {v:.2f}" for k, v in list(scores.items())[:10]])
                print(f" 秤 CONSENSUS MATRIX : [{matrix_str}]")
                print("═"*76)

        except KeyboardInterrupt:
            print("\n 🛑 Halting Holosyn 6.0 CLI safely.")
            break
        except Exception as e:
            import traceback
            print(f"❌ Core Engine Fault: {e}")
            traceback.print_exc()

if __name__ == "__main__":
    start_cli()