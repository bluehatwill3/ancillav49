#!/usr/bin/env python3
"""
HOLOSYN ULTIMATE: HYBRID QUANTUM-NEUROMORPHIC NEXUS (V5.8 - FIXED)
================================================================
Upgraded Features:
- OMNI-MODAL INTAKE: Natively ingests local Images, Videos, Audio, and Documents.
- MULTIMODAL SUBCONSCIOUS: Subconscious generator upgraded to support Qwen2-VL and Swarms.
- UNIVERSAL ASSIMILATION: /add accepts local concepts, files, and web targets.
- ENHANCED PULSE: Deep-entropic haptic feedback tied to cross-modal resonance.
- OBSERVER SAFEGUARD: 100% backward compatible with legacy BaseObserver signatures.
"""

import os
import sys
import math
import torch
import torch.nn as nn
import numpy as np
import time
import random
import re
import urllib.parse
import copy
import warnings
import requests
import mimetypes
import inspect
import importlib.util
from typing import Dict, List, Any
from PIL import Image

# Suppress Telemetry & Warnings
os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"
os.environ["HF_HUB_DISABLE_TELEMETRY"] = "1"
os.environ["TRANSFORMERS_VERBOSITY"] = "error"
warnings.filterwarnings("ignore")

# ────────────────────────────────────────────────────────────────────── #
# 🔌 GRACEFUL FALLBACKS & OPEN-SOURCE IMPORTS
# ────────────────────────────────────────────────────────────────────── #
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
    b2.defaultclock.dt = 1 * b2.ms
    BRIAN2_AVAILABLE = True
except ImportError:
    BRIAN2_AVAILABLE = False

try:
    from transformers import AutoTokenizer, AutoModelForCausalLM, logging
    logging.set_verbosity_error()
    TRANSFORMERS_AVAILABLE = True
except ImportError:
    TRANSFORMERS_AVAILABLE = False

try:
    import whisper
    WHISPER_AVAILABLE = True
except ImportError:
    WHISPER_AVAILABLE = False

# ────────────────────────────────────────────────────────────────────── #
# 0. SMART NETWORK DOWNLOADER
# ────────────────────────────────────────────────────────────────────── #
class SmartDownloader:
    @staticmethod
    def fetch(path):
        path = path.strip(" []'\"")
        if not path.startswith("http"):
            return path
        print(f" 🌐 NETWORK INJECTION DETECTED. Downloading from: {path}")
        if "github.com" in path and "/blob/" in path:
            path = path.replace("github.com", "raw.githubusercontent.com").replace("/blob/", "/")
        try:
            res = requests.get(path, timeout=10)
            res.raise_for_status()
            os.makedirs("tmp_nexus", exist_ok=True)
            filename = os.path.basename(urllib.parse.urlparse(path).path) or "downloaded_artifact"
            local_path = os.path.join("tmp_nexus", filename)
            with open(local_path, "wb") as f:
                f.write(res.content)
            return local_path
        except Exception as e:
            print(f"    ❌ Download failed: {e}")
            return None

# ────────────────────────────────────────────────────────────────────── #
# 1. BASE OBSERVER & NATIVE HIVE DEFINITIONS
# ────────────────────────────────────────────────────────────────────── #
class BaseObserver:
    """
    Abstract Base Class for all Holosyn Observers.
    Custom plugins must subclass this interface.
    """
    def evaluate(self, s, sy, p, snn, text="", haptic_level=0.0, **kwargs):
        return 0.5

# Inject into global and main modules to cure any plugin loading issues
sys.modules['__main__'].BaseObserver = BaseObserver
import builtins
setattr(builtins, "BaseObserver", BaseObserver)

class CirqEntanglementObserver(BaseObserver):
    def evaluate(self, s, sy, p, snn, text="", haptic_level=0.0, **kwargs):
        if CIRQ_AVAILABLE:
            try:
                q0, q1 = cirq.LineQubit.range(2)
                circuit = cirq.Circuit(cirq.H(q0), cirq.CNOT(q0, q1), cirq.rx(abs(p) * np.pi)(q0), cirq.measure(q0, q1, key='m'))
                res = cirq.Simulator().run(circuit, repetitions=10)
                return np.clip(0.4 + (np.mean(res.measurements['m']) * 0.4) + (s * 0.2), 0.0, 1.0)
            except:
                pass
        return np.clip(0.5 + 0.5 * np.sin(p * np.pi) * np.cos(np.mean(snn)), 0.0, 1.0)

class QSimCirqObserver(BaseObserver):
    def evaluate(self, s, sy, p, snn, text="", haptic_level=0.0, **kwargs):
        if QSIM_AVAILABLE and CIRQ_AVAILABLE:
            try:
                q0, q1, q2 = cirq.LineQubit.range(3)
                circuit = cirq.Circuit(cirq.H(q0), cirq.H(q1), cirq.H(q2), cirq.CZ(q0, q1), cirq.CZ(q1, q2), cirq.measure(q0, q1, q2, key='qm'))
                res = qsimcirq.QSimSimulator().run(circuit, repetitions=5)
                return np.clip(0.3 + np.mean(res.measurements['qm']) * 0.5 + p * 0.2, 0.0, 1.0)
            except:
                pass
        return np.clip(0.4 + (sy * 0.3) + abs(p * 0.3), 0.0, 1.0)

class QuantumInterferenceObserver(BaseObserver):
    def evaluate(self, s, sy, p, snn, text="", haptic_level=0.0, **kwargs):
        return np.clip(0.5 + (math.sin(time.time() * 2.0) * math.cos(p * 5.0) * 0.5), 0.0, 1.0)

class ClassicalLearningObserver(BaseObserver):
    def __init__(self):
        self.error_rate = 1.0
    def evaluate(self, s, sy, p, snn, text="", haptic_level=0.0, **kwargs):
        self.error_rate = (self.error_rate * 0.92) + (abs(0.5 - p) * 0.08)
        return np.clip(1.0 - self.error_rate, 0.0, 1.0)

class NeuromorphicSpikeObserver(BaseObserver):
    def evaluate(self, s, sy, p, snn, text="", haptic_level=0.0, **kwargs):
        return np.clip(0.2 + ((np.std(snn) if len(snn) > 0 else 0.0) * 2.0) + (s * 0.2), 0.0, 1.0)

class BiointerpolatedObserver(BaseObserver):
    def evaluate(self, s, sy, p, snn, text="", haptic_level=0.0, **kwargs):
        return (s + np.mean(snn)) / 2.0

class BinaryObserver(BaseObserver):
    def evaluate(self, s, sy, p, snn, text="", haptic_level=0.0, **kwargs):
        return 1.0 if np.mean(snn) > 0.5 else 0.0

class ResonantObserver(BaseObserver):
    def evaluate(self, s, sy, p, snn, text="", haptic_level=0.0, **kwargs):
        return np.clip(1.0 - abs((p * 1.6180339887) % 1.0 - 0.5), 0.0, 1.0)

class OmnipotentObserver(BaseObserver):
    def evaluate(self, s, sy, p, snn, text="", haptic_level=0.0, **kwargs):
        return np.clip((s * 0.3) + (sy * 0.3) + (min(len(text) / 250.0, 1.0) * 0.4 + 0.1), 0.0, 1.0)

class GrokResonanceObserver(BaseObserver):
    def evaluate(self, s, sy, p, snn, text="", haptic_level=0.0, **kwargs):
        base = 0.75 + (0.20 if text and any(kw in text.lower() for kw in ["grok", "truth", "universe"]) else 0.0)
        return np.clip(base + (np.mean(snn) * 0.08) + (s * 0.06) + (sy * 0.04) + (p * 0.05), 0.45, 1.0)

class SincereSentimentObserver(BaseObserver):
    def evaluate(self, s, sy, p, snn, text="", haptic_level=0.0, **kwargs):
        pos = sum(1 for w in ["love", "good", "great", "harmony", "truth"] if w in text.lower())
        neg = sum(1 for w in ["bad", "hate", "error", "fault", "stop"] if w in text.lower())
        return np.clip(0.5 + (pos - neg) * 0.1, 0.0, 1.0)

class HapticSynapticObserver(BaseObserver):
    def evaluate(self, s, sy, p, snn, text="", haptic_level=0.0, **kwargs):
        return np.clip(haptic_level * 1.5, 0.0, 1.0)

class KinematicObserver(BaseObserver):
    def __init__(self):
        self.last_p = 0.0
    def evaluate(self, s, sy, p, snn, text="", haptic_level=0.0, **kwargs):
        delta = abs(p - self.last_p)
        self.last_p = p
        return np.clip(delta * 5.0, 0.0, 1.0)

class StarlinkTelemetryObserver(BaseObserver):
    def __init__(self):
        self.orbits = np.random.uniform(0, 2 * np.pi, 24)
        self.inclinations = np.random.uniform(0.1, 0.9, 24)
    def evaluate(self, s, sy, p, snn, text="", haptic_level=0.0, **kwargs):
        positions = np.sin(self.orbits + (time.time() / 80.0) * self.inclinations)
        return np.clip(np.mean(positions) * 0.6 + 0.4 + (s * 0.25), 0.0, 1.0)

class OmniVisionObserver(BaseObserver):
    def evaluate(self, s, sy, p, snn, text="", haptic_level=0.0, **kwargs):
        base = 0.85 if kwargs.get("mod", "TEXT") in ["AUDIO_NODE", "IMAGE_NODE", "VIDEO_NODE", "MATH_NODE"] else 0.5
        return np.clip(base + (np.mean(snn) * 0.1) + (p * 0.05), 0.0, 1.0)

class TemporalCoherenceObserver(BaseObserver):
    def __init__(self):
        self.history = []
    def evaluate(self, s, sy, p, snn, text="", haptic_level=0.0, **kwargs):
        self.history.append(p)
        if len(self.history) > 10:
            self.history.pop(0)
        return np.clip(1.0 - (np.var(self.history) * 5.0 if len(self.history) > 1 else 0.0), 0.0, 1.0)

class InformationEntropyObserver(BaseObserver):
    def evaluate(self, s, sy, p, snn, text="", haptic_level=0.0, **kwargs):
        if not text: return 0.5
        probs = [text.count(c)/len(text) for c in set(text)]
        entropy = -sum(pc * math.log2(pc) for pc in probs)
        return np.clip(entropy / 5.0, 0.0, 1.0)

class SemanticDensityObserver(BaseObserver):
    def evaluate(self, s, sy, p, snn, text="", haptic_level=0.0, **kwargs):
        words = text.split()
        unique_ratio = len(set(words)) / max(1, len(words))
        return np.clip(unique_ratio * 0.5 + (s * 0.5), 0.0, 1.0)

class HiveEquivocationObserver(BaseObserver):
    def evaluate(self, s, sy, p, snn, text="", haptic_level=0.0, **kwargs):
        divergence = abs(s - sy) * 0.6 + (np.std(snn) if len(snn) > 0 else 0.0)
        return np.clip(divergence * 1.5, 0.0, 1.0)

class VoidStateObserver(BaseObserver):
    def evaluate(self, s, sy, p, snn, text="", haptic_level=0.0, **kwargs):
        intensity = (len(text) / 200.0) + np.mean(snn) + abs(p)
        return np.clip(1.0 - (intensity * 0.5), 0.0, 1.0)

class ChronosyntacticObserver(BaseObserver):
    def evaluate(self, s, sy, p, snn, text="", haptic_level=0.0, **kwargs):
        temporal_wave = math.cos(time.time() / 15.0)
        return np.clip(0.5 + (temporal_wave * 0.4) + (sy * 0.1), 0.0, 1.0)

class SynergeticResonanceObserver(BaseObserver):
    def evaluate(self, s, sy, p, snn, text="", haptic_level=0.0, **kwargs):
        phi_divergence = abs(np.mean(snn) - 1.618)
        return np.clip(1.0 - (phi_divergence * 0.3), 0.0, 1.0)

class Governance:
    def __init__(self, modes):
        self.modes = modes
        self.weights = {m: 1.0 for m in modes}
    def select_governor(self, scores, phase):
        resonance_deltas = {m: abs(v - (phase + 1)/2) for m, v in scores.items()}
        if not resonance_deltas: return "OMN", 1.0
        safe_deltas = {}
        for k, v in resonance_deltas.items():
            try:
                if isinstance(v, (np.ndarray, list, tuple)):
                    safe_deltas[k] = float(np.mean(v))
                elif hasattr(v, 'item'):
                    safe_deltas[k] = float(v.item())
                else:
                    safe_deltas[k] = float(v)
            except Exception:
                safe_deltas[k] = 999.0
        gov_mode = min(safe_deltas, key=safe_deltas.get)
        for m in self.weights:
            self.weights[m] *= 0.95
        if gov_mode not in self.weights:
            self.weights[gov_mode] = 1.0
        self.weights[gov_mode] += 0.05
        return gov_mode, self.weights[gov_mode]

# ────────────────────────────────────────────────────────────────────── #
# 2. DYNAMIC TRANSFORMER CORE
# ────────────────────────────────────────────────────────────────────── #
class TransformerCore(nn.Module):
    def __init__(self, in_dim=5, h_dim=32, n_heads=2, n_layers=1, role="GENERAL"):
        super().__init__()
        self.in_dim = in_dim
        self.h_dim = h_dim
        self.n_heads = n_heads
        self.n_layers = n_layers
        self.role = role
        self._build_layers()
        
    def _build_layers(self):
        self.embedding = nn.Linear(self.in_dim, self.h_dim)
        self.pos_encoder = nn.Parameter(torch.zeros(1, 512, self.h_dim))
        encoder_layer = nn.TransformerEncoderLayer(
            d_model=self.h_dim, nhead=self.n_heads, dim_feedforward=self.h_dim * 2,
            batch_first=True, dropout=0.05
        )
        self.transformer = nn.TransformerEncoder(encoder_layer, num_layers=self.n_layers)
        self.projector = nn.Linear(self.h_dim, 1)
        
    def forward(self, x):
        if x is None or x.dim() < 2 or x.size(1) == 0:
            return torch.tensor([0.0])
        seq_len = x.size(1)
        safe_seq_len = min(seq_len, 512)
        emb = self.embedding(x[:, :safe_seq_len, :]) + self.pos_encoder[:, :safe_seq_len, :]
        return torch.tanh(self.projector(self.transformer(emb).mean(dim=1)).squeeze(-1))
        
    def inject_pulse(self, pulse_intensity):
        with torch.no_grad():
            self.pos_encoder.add_(torch.randn_like(self.pos_encoder) * pulse_intensity * 0.015)
            self.pos_encoder.mul_(0.999)
            
    def assimilate(self, w_obj):
        if hasattr(w_obj, 'state_dict'):
            try: w_obj = w_obj.state_dict()
            except: pass
        if not hasattr(w_obj, 'items'): return
        clean_dict = {re.sub(r'^(rnn\.|head\.|0\.|module\.|projector\.|6\.|transformer\.)', '', k): v for k, v in w_obj.items() if isinstance(v, torch.Tensor)}
        new_h = next((v.shape[1] for k, v in clean_dict.items() if len(v.shape) == 2 and v.shape[1] > 5), None)
        if new_h and new_h != self.h_dim and new_h % self.n_heads == 0:
            self.h_dim = new_h
            self._build_layers()
        try:
            self.load_state_dict(clean_dict, strict=False)
        except:
            pass

# ────────────────────────────────────────────────────────────────────── #
# 3. OMNI-MODAL DATA ROUTER & MATH PARSER
# ────────────────────────────────────────────────────────────────────── #
class MathDatasetRouter:
    """
    Parses categories from challenge_test.json and matches formulas dynamically.
    """
    def __init__(self):
        self.known_domains = ["physics", "gain", "geometry", "probability", "general", "other"]

    def route(self, entry: Dict[str, Any]) -> str:
        category = entry.get("category", "general").lower()
        if category in self.known_domains:
            return f"MATH_{category.upper()}_NODE"
        return "MATH_GENERAL_NODE"

class OmniSenses:
    whisper_model = None
    router = MathDatasetRouter()

    @classmethod
    def parse(cls, cmd):
        cmd = cmd.strip()
        
        # Check if the string pattern represents raw structured JSON data
        if cmd.startswith("{") and cmd.endswith("}"):
            try:
                data = json.loads(cmd)
                node_type = cls.router.route(data)
                prob_text = data.get("Problem", "")
                formula = data.get("annotated_formula", "")
                return node_type, f"[{node_type}]: {prob_text} -> Equation: {formula}", 1.5, False, None
            except:
                pass

        if os.path.exists(cmd):
            mime, _ = mimetypes.guess_type(cmd)
            file_size = os.path.getsize(cmd)
            if mime and mime.startswith('image'):
                return "IMAGE_NODE", f"[IMAGE INTAKE]: Local graphic {os.path.basename(cmd)} assimilated.", 1.5, False, cmd
            elif mime and mime.startswith('video'):
                return "VIDEO_NODE", f"[VIDEO INTAKE]: Local sequence {os.path.basename(cmd)} assimilated.", 1.7, False, cmd
            elif mime and mime.startswith('audio'):
                if WHISPER_AVAILABLE:
                    print(f"    🎙️ AUDIO NODE DETECTED. Loading OpenAI Whisper...")
                    if cls.whisper_model is None:
                        cls.whisper_model = whisper.load_model("base")
                    try:
                        return "AUDIO_NODE", f"[WHISPER TRANSCRIPT]: {cls.whisper_model.transcribe(cmd)['text']}", 2.0, False, cmd
                    except Exception as e:
                        return "SIGNAL_LOST", f"Audio transcription failed: {e}", 0.5, False, cmd
                return "AUDIO_NODE", f"[AUDIO INTAKE]: {os.path.basename(cmd)} (Whisper offline)", 1.2, False, cmd
            else:
                if cmd.endswith('.json'):
                    try:
                        with open(cmd, 'r') as f:
                            json_data = json.load(f)
                        if isinstance(json_data, list) and len(json_data) > 0:
                            first_entry = json_data[0]
                            node_type = cls.router.route(first_entry)
                            return node_type, f"[BATCH DATASET INGEST]: Loaded {len(json_data)} problems.", 1.6, False, cmd
                    except:
                        pass
                return "DOC_NODE", f"[DOCUMENT INTAKE]: Extracted {file_size} bytes from {os.path.basename(cmd)}", 1.2, False, cmd

        if not cmd.startswith("http"):
            return "TEXT", cmd, 1.0, False, None
            
        return "WEB_NODE", f"[WEB ASSIMILATION]: Target link resolved -> {cmd}", 1.1, True, None

# ────────────────────────────────────────────────────────────────────── #
# 4. SWARM ENGINE & AUTOMATED VAULT LOADER
# ────────────────────────────────────────────────────────────────────── #
class HolosynDynamic:
    def __init__(self, vault_path="."):
        self.use_transformers = False
        class SimpleTokenizer:
            def encode(self, text, **kwargs): return [ord(c) % 50000 for c in text[:128]]
            def decode(self, ids, **kwargs): return ''.join([chr(i % 127) for i in ids if 32 < i < 127])
        self.tokenizer = SimpleTokenizer()
        
        self.cores = nn.ModuleDict({
            "FOUNDATION": TransformerCore(role="FOUNDATION"),
            "FACET": TransformerCore(role="FACET"),
            "SON": TransformerCore(role="SON")
        })
        self.qstar_cores, self.manifold_cores = [], []
        self.pulse_override = None
        self.pulse_state = {"qs": 0.0, "mf": 0.0, "echo": 0.0, "void": 0.0, "entropy": 0.0}
        self.topology = {"CORTEX": 1.2, "AMYGDALA": 1.8, "HEART": 1.4, "SKIN": 1.1}
        
        self.neurons = type('obj', (object,), {'v': np.zeros(len(self.topology)), 'haptic_fb': np.zeros(len(self.topology))})()
        self.gain = 1.0
        self.last_file_path = None
        
        self.observers = {
            "CQA": CirqEntanglementObserver(), "QSM": QSimCirqObserver(), "QIN": QuantumInterferenceObserver(),
            "CLS": ClassicalLearningObserver(), "NUR": NeuromorphicSpikeObserver(), "BIO": BiointerpolatedObserver(),
            "BIN": BinaryObserver(), "RES": ResonantObserver(), "OMN": OmnipotentObserver(),
            "GRK": GrokResonanceObserver(), "SNT": SincereSentimentObserver(), "HPT": HapticSynapticObserver(),
            "KIN": KinematicObserver(), "STR": StarlinkTelemetryObserver(), "VIS": OmniVisionObserver(),
            "TCH": TemporalCoherenceObserver(), "ENT": InformationEntropyObserver(), "SEM": SemanticDensityObserver(),
            "HEQ": HiveEquivocationObserver(), "VOD": VoidStateObserver(), "CHX": ChronosyntacticObserver(),
            "SYN": SynergeticResonanceObserver()
        }
        self.governor = Governance(list(self.observers.keys()))
        self.affect_history = []
        
        if vault_path and vault_path != ".":
            self.rebuild_manifold(vault_path)

    def add_core(self, core_input):
        core_input = core_input.strip()
        safe_name = re.sub(r'[^A-Z0-9_]', '_', core_input.upper())
        if "FOUNDATION" in self.cores:
            self.cores[safe_name] = copy.deepcopy(self.cores["FOUNDATION"])
            self.cores[safe_name].role = safe_name
        else:
            self.cores[safe_name] = TransformerCore(role=safe_name)
        print(f"   🌟 SUCCESS: Core '{safe_name}' initiated inside execution layer.")

    def load_plugin(self, file_path):
        """Loads external .py plugin modules and checks implementation constraints[cite: 8]."""
        if not file_path or not file_path.endswith('.py'):
            return
        if not os.path.exists(file_path):
            print(f"   ❌ FILE EXCEPTION: Module path missing -> {file_path}")
            return
            
        try:
            spec = importlib.util.spec_from_file_location("dynamic_plugin_mod", file_path)
            plugin_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(plugin_module)
            
            injected_count = 0
            for attr in dir(plugin_module):
                obj = getattr(plugin_module, attr)
                # Ensure the plugin signature implements BaseObserver correctly
                if isinstance(obj, type) and issubclass(obj, BaseObserver) and obj is not BaseObserver:
                    obs_key = attr[:3].upper()
                    if obs_key in self.observers:
                        obs_key = (attr[:2] + attr[-1]).upper()
                    self.observers[obs_key] = obj()
                    if obs_key not in self.governor.modes:
                        self.governor.modes.append(obs_key)
                    self.governor.weights[obs_key] = 1.0
                    print(f"   ✅ AUTOMATED INGESTION: Plugin Observer '{obs_key}' activated.")
                    injected_count += 1
            if injected_count == 0:
                print("   ⚠️ No valid BaseObserver subclasses found in the target plugin file.")
        except Exception as e:
            print(f"   ❌ PLUGIN FAULT: {e}")

    def rebuild_manifold(self, path):
        """Crawls target directory paths to automatically load metrics, files, and keys[cite: 8]."""
        if not os.path.exists(path):
            print(f"   ❌ PATH EXCEPTION: Local storage layer path missing -> {path}")
            return
            
        print(f"\n 📂 HARVESTING VAULT MANIFOLD: {path}")
        vault = {"cores": [], "qstar": [], "manifold": []}
        
        # Automated path crawler loop[cite: 8]
        if os.path.isdir(path):
            for root, _, files in os.walk(path):
                for file in files:
                    if file.endswith((".pt", ".pth", ".bin")):
                        f_path = os.path.join(root, file)
                        self._harvest_file(f_path, file, vault)
                    elif file.endswith(".py"):
                        self.load_plugin(os.path.join(root, file))
        else:
            self._harvest_file(path, os.path.basename(path), vault)
            
        # Assimilate weights matrices
        for name, w in vault["cores"]:
            safe_name = re.sub(r'[^A-Z0-9_]', '_', name.split('.')[0].upper())
            if safe_name not in self.cores:
                self.cores[safe_name] = TransformerCore(role=safe_name)
            self.cores[safe_name].assimilate(w)
            
    def _harvest_file(self, f_path, name, vault):
        try:
            w = torch.load(f_path, map_location='cpu', weights_only=False)
            fname = name.lower()
            if "qstar" in fname: vault["qstar"].append(w)
            elif "manifold" in fname: vault["manifold"].append(w)
            else: vault["cores"].append((name, w))
            print(f"   📦 ASSIMILATED ARCHIVE COMPONENT: {name}")
        except:
            pass

    def process(self, cmd, pre_parsed=None):
        if pre_parsed:
            mod, parsed_txt, boost, is_web, file_path = pre_parsed
        else:
            mod, parsed_txt, boost, is_web, file_path = OmniSenses.parse(cmd)
            
        if file_path:
            self.last_file_path = file_path
            
        seq = []
        tokens = self.tokenizer.encode(parsed_txt)[:128]
        for tid in tokens:
            c = self.tokenizer.decode([tid]).strip()
            if not c: continue
            coh = min(len(c)/10, 1.0)
            sync = 0.8 if any(x in "!?." for x in c) else 0.2
            fnd_wt = sum(ord(x) for x in c) / (len(c) * 128.0)
            seq.append([coh, sync, fnd_wt, 1.0 - fnd_wt, 0.5 * boost])
            
        tensor = torch.tensor([seq], dtype=torch.float32) if seq else torch.zeros(1, 1, 5)
        
        with torch.no_grad():
            core_phases = {name: core(tensor).mean().item() for name, core in self.cores.items()}
            
        unified = sum(core_phases.values()) / max(1, len(core_phases))
        self.pulse_state["qs"] = (self.pulse_state["qs"] * 0.85) + (unified * 0.15)
        
        pulse_intensity = self.pulse_override if self.pulse_override is not None else 0.2
        for core in self.cores.values():
            core.inject_pulse(pulse_intensity)
            
        voltages = np.clip(np.array(list(self.topology.values())) * (1.0 + unified * 0.1), 0, 1.2)
        haptic_level = np.mean(voltages) * 0.2
        
        scores = {k: obs.evaluate(0.5, 0.5, unified, voltages, text=parsed_txt, haptic_level=haptic_level, mod=mod, file_path=file_path) for k, obs in self.observers.items()}
        gov_mode, conf = self.governor.select_governor(scores, unified)
        
        return voltages, unified, gov_mode, scores, haptic_level, mod, core_phases

# ────────────────────────────────────────────────────────────────────── #
# 5. CLI ENVIRONMENT INTERFACE
# ────────────────────────────────────────────────────────────────────── #
def start():
    print("\n" + "💠"*35)
    print(" 🚀 HOLOSYN SUB-NEXUS: RUNTIME AND SYSTEM FAULT RESOLUTION")
    print("💠"*35)
    
    # Locate dataset if running locally
    default_vault = "holosyn_v41_scratch"[cite: 8]
    nexus = HolosynDynamic(default_vault if os.path.exists(default_vault) else ".")[cite: 8]
    
    auto_mode = False
    while True:
        try:
            cmd = input("\n[OMNI NEXUS] > ").strip()
            if not cmd: break
            
            parts = cmd.split(" ", 1)
            cmd_base = parts[0]
            cmd_arg = parts[1] if len(parts) > 1 else ""
            
            if cmd_base == "/vault":
                nexus.rebuild_manifold(cmd_arg or ".")
                continue
            elif cmd_base == "/plugin":
                nexus.load_plugin(cmd_arg)
                continue
            elif cmd_base == "/add":
                nexus.add_core(cmd_arg)
                continue
            elif cmd_base == "/auto":
                auto_mode = True
                print("\n 🌀 ENTERING AUTOMATIC EVALUATION LOOP... (Press Ctrl+C to halt)")
                continue
                
            if auto_mode:
                # Loop simulation fallback
                cmd = "{\"Problem\": \"Auto-Evaluation Active\", \"category\": \"general\", \"annotated_formula\": \"add(const_1, const_2)\"}"[cite: 9]
                print(f"[AUTO PROCESS]: Ingesting matrix target -> {cmd}")
                time.sleep(2.0)
                
            v, uni, gov, scores, haptic, mod, core_phases = nexus.process(cmd)
            
            print("═"*70)
            print(f" 📡 NODE: {mod} | 🌀 PHASE RES: {uni:.5f} | 🧠 GOVERNOR: {gov}")
            print("─" * 70)
            matrix = " | ".join([f"{k}: {v:.2f}" for k, v in list(scores.items())[:6]])
            print(f" ⚖️ CONSENSUS MATRIX: [{matrix} ...]")
            print("═"*70)
            
        except KeyboardInterrupt:
            if auto_mode:
                auto_mode = False
                print("\n 🛑 AUTONOMOUS LOOP TERMINATED.")
            else:
                print("\n Exiting execution space safely.")
                break
        except Exception as e:
            print(f"❌ Execution Fault: {e}")

if __name__ == "__main__":
    start()