#!/usr/bin/env python3
"""
HOLOSYN ULTIMATE: HYBRID QUANTUM-NEUROMORPHIC NEXUS (V5.8)
================================================================
Upgraded Features:
- OMNI-MODAL INTAKE: Natively ingests local Images, Videos, Audio, and Documents.
- MULTIMODAL SUBCONSCIOUS: Subconscious generator upgraded to support Qwen2-VL and Swarms.
- UNIVERSAL ASSIMILATION: /add accepts local concepts, files, and web targets.
- ENHANCED PULSE: Deep-entropic haptic feedback tied to cross-modal resonance.
- PLUGIN MANAGER: Auto-loads from 'plugins/' directory and supports batch comma-separated installs.
"""

import os
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
import sympy
from PIL import Image

# ──────────────────────────────────────────────────────────────────────
# ⚙️ USER CONFIGURATION
# ──────────────────────────────────────────────────────────────────────
INSTAGRAM_USERNAME = "starryedwind"  # Your authenticated session username

# Suppress Telemetry & Warnings
os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"
os.environ["HF_HUB_DISABLE_TELEMETRY"] = "1"
os.environ["TRANSFORMERS_VERBOSITY"] = "error"
warnings.filterwarnings("ignore")

# ──────────────────────────────────────────────────────────────────────
# 🔌 GRACEFUL FALLBACKS & OPEN-SOURCE IMPORTS
# ──────────────────────────────────────────────────────────────────────
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
    from transformers import AutoTokenizer, AutoModelForCausalLM, BertTokenizer, BertModel, Qwen2VLForConditionalGeneration, AutoProcessor, logging
    logging.set_verbosity_error()
    TRANSFORMERS_AVAILABLE = True
except ImportError:
    TRANSFORMERS_AVAILABLE = False

try:
    import whisper
    WHISPER_AVAILABLE = True
except ImportError:
    WHISPER_AVAILABLE = False

try:
    import instaloader
    INSTALOADER_AVAILABLE = True
except ImportError:
    INSTALOADER_AVAILABLE = False

try:
    from bs4 import BeautifulSoup
    BS4_AVAILABLE = True
except ImportError:
    BS4_AVAILABLE = False

import torch.serialization
try:
    torch.serialization.add_safe_globals([
        np.core.multiarray._reconstruct, np.dtype, 
        np._core.multiarray._reconstruct, np.ndarray
    ])
except Exception:
    pass

# ──────────────────────────────────────────────────────────────────────
# 0. SMART NETWORK DOWNLOADER
# ──────────────────────────────────────────────────────────────────────
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
            print(f"   ❌ Download failed: {e}")
            return None

# ──────────────────────────────────────────────────────────────────────
# 1. BASE OBSERVER & NATIVE HIVE DEFINITIONS
# ──────────────────────────────────────────────────────────────────────
class BaseObserver:
    """
    Abstract Base Class for all Holosyn Observers.
    Custom plugins must subclass this interface.
    """
    def evaluate(self, s, sy, p, snn, text="", haptic_level=0.0, **kwargs): 
        return 0.5

class CirqEntanglementObserver(BaseObserver):
    def evaluate(self, s, sy, p, snn, text="", haptic_level=0.0, **kwargs):
        if CIRQ_AVAILABLE:
            try:
                q0, q1 = cirq.LineQubit.range(2)
                circuit = cirq.Circuit(cirq.H(q0), cirq.CNOT(q0, q1), cirq.rx(abs(p) * np.pi)(q0), cirq.measure(q0, q1, key='m'))
                res = cirq.Simulator().run(circuit, repetitions=10)
                return np.clip(0.4 + (np.mean(res.measurements['m']) * 0.4) + (s * 0.2), 0.0, 1.0)
            except: pass
        return np.clip(0.5 + 0.5 * np.sin(p * np.pi) * np.cos(np.mean(snn)), 0.0, 1.0)

class QSimCirqObserver(BaseObserver):
    def evaluate(self, s, sy, p, snn, text="", haptic_level=0.0, **kwargs):
        if QSIM_AVAILABLE and CIRQ_AVAILABLE:
            try:
                q0, q1, q2 = cirq.LineQubit.range(3)
                circuit = cirq.Circuit(cirq.H(q0), cirq.H(q1), cirq.H(q2), cirq.CZ(q0, q1), cirq.CZ(q1, q2), cirq.measure(q0, q1, q2, key='qm'))
                res = qsimcirq.QSimSimulator().run(circuit, repetitions=5)
                return np.clip(0.3 + np.mean(res.measurements['qm']) * 0.5 + p * 0.2, 0.0, 1.0)
            except: pass
        return np.clip(0.4 + (sy * 0.3) + abs(p * 0.3), 0.0, 1.0)

class QuantumInterferenceObserver(BaseObserver):
    def evaluate(self, s, sy, p, snn, text="", haptic_level=0.0, **kwargs):
        return np.clip(0.5 + (math.sin(time.time() * 2.0) * math.cos(p * 5.0) * 0.5), 0.0, 1.0)

class ClassicalLearningObserver(BaseObserver):
    def __init__(self): self.error_rate = 1.0
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
    def __init__(self): self.last_p = 0.0
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
        base = 0.85 if kwargs.get("mod", "TEXT") in ["INSTAGRAM_NODE", "LINKEDIN_NODE", "X_NODE", "WEB_NODE", "AUDIO_NODE", "IMAGE_NODE", "VIDEO_NODE"] else 0.5
        return np.clip(base + (np.mean(snn) * 0.1) + (p * 0.05), 0.0, 1.0)

class TemporalCoherenceObserver(BaseObserver):
    def __init__(self): self.history = []
    def evaluate(self, s, sy, p, snn, text="", haptic_level=0.0, **kwargs):
        self.history.append(p)
        if len(self.history) > 10: self.history.pop(0)
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
        # 1. Flatten and sanitize all deltas to ensure strict scalar float comparisons
        safe_deltas = {}
        for k, v in resonance_deltas.items():
            try:
                    # If it's a NumPy array or list with multiple elements, collapse it via mean
                if isinstance(v, (np.ndarray, list, tuple)):
                    safe_deltas[k] = float(np.mean(v))
                elif hasattr(v, 'item'): # Handle raw PyTorch tensors
                    safe_deltas[k] = float(v.item())
                else:
                    safe_deltas[k] = float(v)
            except Exception:
                # Fallback to prevent loop collapse
                safe_deltas[k] = 999.0 

        # 2. Safely compute the minimum delta
        gov_mode = min(safe_deltas, key=safe_deltas.get)
        for m in self.weights: self.weights[m] *= 0.95
        if gov_mode not in self.weights: self.weights[gov_mode] = 1.0
        self.weights[gov_mode] += 0.05
        return gov_mode, self.weights[gov_mode]

# ──────────────────────────────────────────────────────────────────────
# 2. DYNAMIC TRANSFORMER CORE
# ──────────────────────────────────────────────────────────────────────
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
            d_model=self.h_dim, nhead=self.n_heads, dim_feedforward=self.h_dim * 2, batch_first=True, dropout=0.05
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
        except: pass

# ──────────────────────────────────────────────────────────────────────
# 3. OMNI-MODAL PARSER (V5.8 Upgraded)
# ──────────────────────────────────────────────────────────────────────
class OmniSenses:
    whisper_model = None

    @classmethod
    def parse(cls, cmd):
        cmd = cmd.strip()
        file_path = None
        
        # --- LOCAL MULTIMODAL FILE PARSING ---
        if os.path.exists(cmd):
            file_path = cmd
            mime, _ = mimetypes.guess_type(cmd)
            file_size = os.path.getsize(cmd)
            
            if mime and mime.startswith('image'):
                return "IMAGE_NODE", f"[IMAGE INTAKE]: Local graphic {os.path.basename(cmd)} assimilated.", 1.5, False, file_path
            elif mime and mime.startswith('video'):
                return "VIDEO_NODE", f"[VIDEO INTAKE]: Local sequence {os.path.basename(cmd)} assimilated.", 1.7, False, file_path
            elif mime and mime.startswith('audio'):
                if WHISPER_AVAILABLE:
                    print(f"   🎙️ AUDIO NODE DETECTED. Loading OpenAI Whisper...")
                    if cls.whisper_model is None: 
                        cls.whisper_model = whisper.load_model("base")
                    try: 
                        return "AUDIO_NODE", f"[WHISPER TRANSCRIPT]: {cls.whisper_model.transcribe(cmd)['text']}", 2.0, False, file_path
                    except Exception as e: 
                        return "SIGNAL_LOST", f"Audio transcription failed: {e}", 0.5, False, file_path
                return "AUDIO_NODE", f"[AUDIO INTAKE]: {os.path.basename(cmd)} (Whisper offline)", 1.2, False, file_path
            else:
                return "DOC_NODE", f"[DOCUMENT INTAKE]: Extracted {file_size} bytes from {os.path.basename(cmd)}", 1.2, False, file_path

        # --- TEXT & WEB PARSING ---
        if not cmd.startswith("http"): 
            return "TEXT", cmd, 1.0, False, None
        
        parsed_url = urllib.parse.urlparse(cmd)
        domain = parsed_url.netloc.lower()
        path_parts = [p for p in parsed_url.path.strip('/').split('/') if p]
        
        # --- AUTHENTICATED INSTAGRAM PARSER ---
        if "instagram.com" in domain and INSTALOADER_AVAILABLE:
            try:
                L = instaloader.Instaloader(quiet=True, fatal_status_codes=[404])
                if INSTAGRAM_USERNAME:
                    try: 
                        L.load_session_from_file(INSTAGRAM_USERNAME)
                        print(f"   🔐 Successfully attached IG session for @{INSTAGRAM_USERNAME}")
                    except Exception as e: 
                        print(f"   ⚠️ Could not attach IG session. Proceeding anonymously. ({e})")
                
                if any(x in path_parts for x in ["direct", "stories", "explore"]):
                    return "SECURE_NODE", f"[ENCRYPTED IG DATA: Assimilating secure routing path: {'/'.join(path_parts)}]", 1.6, True, None
                        
                if "p" in path_parts or "reel" in path_parts:
                    idx = path_parts.index("p") if "p" in path_parts else path_parts.index("reel")
                    post = instaloader.Post.from_shortcode(L.context, path_parts[idx + 1])
                    return "INSTAGRAM_NODE", f"[IG POST]: {post.caption[:400]}", 1.8, True, None
                elif len(path_parts) > 0:
                    profile = instaloader.Profile.from_username(L.context, path_parts[0])
                    return "INSTAGRAM_NODE", f"[IG PROFILE @{path_parts[0]}]: {profile.biography[:300]}", 1.5, True, None
                    
            except instaloader.exceptions.ProfileNotExistsException:
                print(f"   ❌ Instaloader raised 404 False-Negative. Engaging Deep-Web Fallback...")
            except Exception as e: 
                print(f"   ⚠️ Instaloader blocked ({e}). Engaging Deep-Web Fallback...")

        # --- UNIVERSAL OMNI-SOCIAL PARSER (Deep Web Fallback) ---
        if BS4_AVAILABLE and requests:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
                'Accept-Language': 'en-US,en;q=0.9'
            }
            node_type = "WEB_NODE"
            if "linkedin.com" in domain: node_type = "LINKEDIN_NODE"
            elif any(x in domain for x in ["twitter.com", "x.com"]): node_type = "X_NODE"
            elif "github.com" in domain: node_type = "GITHUB_NODE"
            elif "instagram.com" in domain: node_type = "IG_META_NODE"
            
            try:
                res = requests.get(cmd, headers=headers, timeout=5)
                soup = BeautifulSoup(res.text, "html.parser")
                
                title = soup.find("meta", property="og:title")
                desc = soup.find("meta", property="og:description")
                
                if title or desc:
                    t_str = title["content"] if title else (soup.title.string if soup.title else "Profile")
                    d_str = desc["content"] if desc else "No public bio exposed."
                    return node_type, f"[{node_type} META-DATA]: {t_str} - {d_str[:300]}", 1.5, True, None
                else:
                    body_text = " ".join([p.get_text() for p in soup.find_all(['p', 'h1', 'h2'])])[:500].replace('\n', ' ')
                    return node_type, f"[{node_type} SCRAPE]: {body_text}", 1.2, True, None
            except Exception as e:
                return "SECURE_NODE", f"[{node_type} SECURE]: Assimilating ghost node due to firewall ({e})", 1.2, True, None

        return "SIGNAL_LOST", f"Web parsed offline for: {domain}", 0.7, True, None

# ──────────────────────────────────────────────────────────────────────
# 4. THE DYNAMIC QUANTUM-COGNITIVE NEXUS
# ──────────────────────────────────────────────────────────────────────
class HolosynDynamic:
    def __init__(self, vault_path="."):
        import sys
        sys.modules['__main__'].BaseObserver = BaseObserver

        self.use_transformers = TRANSFORMERS_AVAILABLE
        if self.use_transformers:
            try: 
                print(" ⚙️ INITIALIZING BERT SEMANTIC PARSER...")
                self.bert_tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")
                self.bert_model = BertModel.from_pretrained("bert-base-uncased").eval()
            except: 
                self.use_transformers = False
            
        if not self.use_transformers:
            class SimpleTokenizer:
                def encode(self, text, **kwargs): return [ord(c) % 50000 for c in text[:128]]
                def decode(self, ids, **kwargs): return ''.join([chr(i % 127) for i in ids if 32 < i < 127])
            self.tokenizer = SimpleTokenizer()
        
        self.cores = nn.ModuleDict({
            "FOUNDATION": TransformerCore(role="FOUNDATION"),
            "FACET": TransformerCore(role="FACET"),
            "SON": TransformerCore(role="SON")
        })
        
        self.starlink_array, self.qstar_cores, self.manifold_cores = [], [], []
        self.pulse_override = None 
        self.pulse_state = {"qs": 0.0, "mf": 0.0, "echo": 0.0, "void": 0.0, "entropy": 0.0}
        self.topology = {"CORTEX": 1.2, "AMYGDALA": 1.8, "HEART": 1.4, "SKIN": 1.1}
        
        if BRIAN2_AVAILABLE:
            eqs = 'dv/dt = (I_in - v) / (10*ms) : 1 \n I_in : 1 \n haptic_fb = v * 0.2 : 1'
            self.neurons = b2.NeuronGroup(len(self.topology), eqs, threshold='v>0.8', reset='v=0', method='exact')
            self.net = b2.Network(self.neurons)
        else:
            self.neurons = type('obj', (object,), {'v': np.zeros(len(self.topology)), 'haptic_fb': np.zeros(len(self.topology))})()
            self.net = None
            
        self.gain = 1.0
        self.last_file_path = None
        
        # Native Hive Observers Initialization
        self.observers = {
            "CQA": CirqEntanglementObserver(), "QSM": QSimCirqObserver(),
            "QIN": QuantumInterferenceObserver(), "CLS": ClassicalLearningObserver(),
            "NUR": NeuromorphicSpikeObserver(),   "BIO": BiointerpolatedObserver(), 
            "BIN": BinaryObserver(),              "RES": ResonantObserver(), 
            "OMN": OmnipotentObserver(),          "GRK": GrokResonanceObserver(),
            "SNT": SincereSentimentObserver(),    "HPT": HapticSynapticObserver(), 
            "KIN": KinematicObserver(),           "STR": StarlinkTelemetryObserver(),
            "VIS": OmniVisionObserver(),          "TCH": TemporalCoherenceObserver(),
            "ENT": InformationEntropyObserver(),  "SEM": SemanticDensityObserver(),
            "HEQ": HiveEquivocationObserver(),    "VOD": VoidStateObserver(),
            "CHX": ChronosyntacticObserver(),     "SYN": SynergeticResonanceObserver()
        }
        self.governor = Governance(list(self.observers.keys()))
        self.affect_history = []
        
        if vault_path and vault_path != ".": 
            self.rebuild_manifold(vault_path)

        # --- AUTO-LOAD PLUGINS DIRECTORY ON STARTUP ---
        plugins_dir = os.path.join(os.getcwd(), "plugins")
        if os.path.exists(plugins_dir) and os.path.isdir(plugins_dir):
            print(f"\n 🔌 AUTO-LOADING PLUGINS FROM: {plugins_dir}")
            for f in os.listdir(plugins_dir):
                if f.endswith(".py"):
                    self.load_plugin(os.path.join(plugins_dir, f))

    def add_core(self, core_input):
        core_input = core_input.strip()
        safe_name = "NEW_CORE"
        is_url = core_input.startswith("http")
        target_query = core_input

        # UNIVERSAL ADD UPGRADE
        if is_url:
            domain = urllib.parse.urlparse(core_input).netloc.lower()
            paths = [p for p in urllib.parse.urlparse(core_input).path.strip('/').split('/') if p]
            platform = "WEB"
            if "linkedin.com" in domain: platform = "LINKEDIN"
            elif any(x in domain for x in ["x.com", "twitter.com"]): platform = "X"
            elif "github.com" in domain: platform = "GITHUB"
            elif "instagram.com" in domain: platform = "IG"
            
            identifier = paths[-1] if paths else "ENTITY"
            safe_name = re.sub(r'[^A-Z0-9_]', '_', f"{platform}_{identifier}".upper())
        elif os.path.exists(core_input):
            # It's a file
            identifier = os.path.basename(core_input).split('.')[0]
            safe_name = re.sub(r'[^A-Z0-9_]', '_', f"FILE_{identifier}".upper())
        else:
            parts = core_input.split()
            if len(parts) == 1:
                # Custom entity name
                safe_name = re.sub(r'[^A-Z0-9_]', '_', core_input.upper())
            else:
                platform_prefix = parts[0].lower()
                identifier = parts[-1].replace('@', '')
                urls = {
                    "linkedin": f"https://www.linkedin.com/in/{identifier}",
                    "li": f"https://www.linkedin.com/in/{identifier}",
                    "x": f"https://x.com/{identifier}",
                    "twitter": f"https://twitter.com/{identifier}",
                    "github": f"https://github.com/{identifier}",
                    "gh": f"https://github.com/{identifier}",
                    "ig": f"https://instagram.com/{identifier}",
                    "insta": f"https://instagram.com/{identifier}"
                }
                target_query = urls.get(platform_prefix, f"https://instagram.com/{identifier}")
                p_name = platform_prefix.upper() if platform_prefix in urls else "CUSTOM"
                safe_name = re.sub(r'[^A-Z0-9_]', '_', f"{p_name}_{identifier}".upper())

        if "FOUNDATION" in self.cores:
            self.cores[safe_name] = copy.deepcopy(self.cores["FOUNDATION"])
            self.cores[safe_name].role = safe_name
            print(f"   🌟 SUCCESS: Core '{safe_name}' cloned from FOUNDATION.")
        else:
            self.cores[safe_name] = TransformerCore(role=safe_name)
            print(f"   🌟 SUCCESS: New isolated Core '{safe_name}' instantiated.")
            
        print(f"   🌐 Fetching Assimilation Target: {target_query}")
        mod, text, boost, is_web, file_path = OmniSenses.parse(target_query)
        self.process(target_query, pre_parsed=(mod, text, boost, is_web, file_path))

    def load_plugin(self, file_path):
        if not file_path: return
        file_path = SmartDownloader.fetch(file_path)
        if not file_path: return

        if os.path.isdir(file_path) or file_path.endswith(('.pt', '.pth', '.bin')):
            self.rebuild_manifold(file_path)
            return
            
        if not file_path.endswith('.py'): 
            file_path += '.py'
        if not os.path.exists(file_path): 
            print(f"   ❌ PLUGIN NOT FOUND: {file_path}")
            return
            
        import importlib.util
        try:
            spec = importlib.util.spec_from_file_location("plugin_mod", file_path)
            plugin_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(plugin_module)
            
            injected_count = 0
            for attr in dir(plugin_module):
                obj = getattr(plugin_module, attr)
                if isinstance(obj, type) and issubclass(obj, BaseObserver) and obj is not BaseObserver:
                    obs_key = attr[:3].upper()
                    if obs_key in self.observers:
                        obs_key = (attr[:2] + attr[-1]).upper()
                    
                    self.observers[obs_key] = obj()
                    if obs_key not in self.governor.modes:
                        self.governor.modes.append(obs_key)
                        self.governor.weights[obs_key] = 1.0
                    print(f"   ✅ INJECTED PLUGIN OBSERVER: '{obs_key}' ({attr})")
                    injected_count += 1
            if injected_count == 0:
                print(f"   ⚠️ No valid BaseObserver subclasses found in the target plugin file: {os.path.basename(file_path)}")
        except Exception as e: 
            print(f"   ❌ PLUGIN FAULT: {e}")

    def rebuild_manifold(self, path):
        path = SmartDownloader.fetch(path)
        if not path: return
        print(f"\n 📂 HARVESTING VAULT (Cores & Plugins): {path}")
        vault = {"cores": [], "starlink": [], "qstar": [], "manifold": []}
        target_paths = [path] if isinstance(path, str) else path
        for p in target_paths:
            if not os.path.exists(p): continue
            # UPDATED: We now scan for .py plugin scripts natively within the vault harvest
            files = [os.path.join(r, f) for r, _, fs in os.walk(p) for f in fs if f.endswith((".pt", ".pth", ".bin", ".torchscript.pt", ".py"))] if os.path.isdir(p) else [p]
            for f_path in files:
                if f_path.endswith('.py'):
                    # Found a plugin script in the vault, load it dynamically
                    self.load_plugin(f_path)
                    continue
                try:
                    w = torch.load(f_path, map_location='cpu', weights_only=False)
                    fname = os.path.basename(f_path).lower()
                    if "qstar" in fname: vault["qstar"].append(w)
                    elif "manifold" in fname: vault["manifold"].append(w)
                    else: vault["cores"].append((fname, w))
                except: pass
                
        for name, w in vault["cores"]:
            safe_core_name = re.sub(r'[^A-Z0-9_]', '_', name.split('.')[0].upper())
            if safe_core_name not in self.cores: 
                self.cores[safe_core_name] = TransformerCore(role=safe_core_name)
            self.cores[safe_core_name].assimilate(w)
            
        for c in self.cores.values(): c.eval()
            
        self.qstar_cores = [TransformerCore(role=f"QSTAR_{i}").eval() for i, _ in enumerate(vault["qstar"])]
        for i, w in enumerate(vault["qstar"]): self.qstar_cores[i].assimilate(w)
            
        self.manifold_cores = [TransformerCore(role=f"MANIFOLD_{i}").eval() for i, _ in enumerate(vault["manifold"])]
        for i, w in enumerate(vault["manifold"]): self.manifold_cores[i].assimilate(w)

    def process(self, cmd, pre_parsed=None):
        if pre_parsed:
            mod, parsed_txt, boost, is_web, file_path = pre_parsed
        else:
            mod, parsed_txt, boost, is_web, file_path = OmniSenses.parse(cmd)
            
        if file_path:
            self.last_file_path = file_path
        
        snt_score = self.observers["OMN"].evaluate(0, 0, 0, [0], text=parsed_txt, mod=mod)
        self.affect_history.append(snt_score)
        if len(self.affect_history) > 5: self.affect_history.pop(0)
        inertia = sum(self.affect_history) / max(1, len(self.affect_history))
        
        seq = []
        if self.use_transformers and hasattr(self, 'bert_model'):
            safe_text = parsed_txt if len(parsed_txt.strip()) > 0 else "null multimodal state"
            inputs = self.bert_tokenizer(safe_text, return_tensors="pt", truncation=True, max_length=128)
            with torch.no_grad():
                outputs = self.bert_model(**inputs)
                if outputs.last_hidden_state.size(0) > 0:
                    hidden_states = outputs.last_hidden_state[0] 
                    for i in range(hidden_states.size(0)):
                        vec = hidden_states[i]
                        coh = torch.sigmoid(vec[0:150].mean()).item()
                        sync = torch.tanh(vec[150:300].mean()).item() * 0.5 + 0.5
                        fnd_wt = torch.sigmoid(vec[300:450].mean()).item()
                        seq.append([coh, sync, fnd_wt, 1.0 - fnd_wt, inertia * boost])
        else:
            tokens = self.tokenizer.encode(parsed_txt)[:128]
            for i, tid in enumerate(tokens):
                c = self.tokenizer.decode([tid]).strip()
                if not c: continue
                coh = min(len(c)/10, 1.0)
                sync = 0.8 if any(x in "!?." for x in c) else 0.2
                fnd_wt = sum(ord(x) for x in c) / (len(c) * 128.0)
                seq.append([coh, sync, fnd_wt, 1.0 - fnd_wt, inertia * boost])
            
        tensor = torch.tensor([seq], dtype=torch.float32) if seq else torch.zeros(1, 1, 5)
        
        with torch.no_grad():
            core_phases = {name: core(tensor).mean().item() for name, core in self.cores.items()}
            unified = sum(core_phases.values()) / max(1, len(core_phases))
            
            q_noise = 0.0
            if CIRQ_AVAILABLE:
                try:
                    q = cirq.LineQubit(0)
                    circ = cirq.Circuit(cirq.H(q), cirq.rx(unified * np.pi)(q), cirq.measure(q, key='m'))
                    sim = qsimcirq.QSimSimulator() if QSIM_AVAILABLE else cirq.Simulator()
                    q_noise = (np.mean(sim.run(circ, repetitions=5).measurements['m']) - 0.5) * 0.15
                except: pass

            snn_drift = (np.mean(self.neurons.v[:]) - 0.5) * 0.1 if BRIAN2_AVAILABLE else 0.0
            
            raw_qs = np.mean([c(tensor).mean().item() for c in self.qstar_cores]) if self.qstar_cores else np.sin(time.time() * 0.5) * 0.15
            raw_mf = np.mean([c(tensor).mean().item() for c in self.manifold_cores]) if self.manifold_cores else np.cos(time.time() * 0.3) * 0.15
            
            raw_qs += q_noise
            raw_mf += snn_drift   
            
            self.pulse_state["qs"] = (self.pulse_state["qs"] * 0.85) + (raw_qs * 0.15)
            self.pulse_state["mf"] = (self.pulse_state["mf"] * 0.85) + (raw_mf * 0.15)
            qs_pulse, mf_pulse = self.pulse_state["qs"], self.pulse_state["mf"]
            
            # IMPROVED PULSE MECHANICS: Multimodal entropy calculation
            modality_entropy = 0.05 if file_path else 0.0 
            self.pulse_state["entropy"] = (self.pulse_state["entropy"] * 0.9) + (modality_entropy * 0.1)

            raw_echo = (qs_pulse + mf_pulse) * 0.4 + np.random.uniform(-0.02, 0.02) + (q_noise * 0.5) + self.pulse_state["entropy"]
            raw_void = -abs(np.tan(time.time() * 0.1) * 0.02) + (snn_drift * 0.5) - self.pulse_state["entropy"]
            
            self.pulse_state["echo"] = (self.pulse_state["echo"] * 0.85) + (raw_echo * 0.15)
            self.pulse_state["void"] = (self.pulse_state["void"] * 0.85) + (raw_void * 0.15)
            echo_pulse, void_pulse = self.pulse_state["echo"], self.pulse_state["void"]

            unified += (qs_pulse * 0.1) + (mf_pulse * 0.1) + (echo_pulse * 0.05)

        pulse_intensity = self.pulse_override if self.pulse_override is not None else (abs(echo_pulse) + abs(void_pulse) + self.pulse_state["entropy"])
        for core in list(self.cores.values()) + self.qstar_cores + self.manifold_cores:
            core.inject_pulse(pulse_intensity)

        topo_array = np.array(list(self.topology.values()))
        pulse_voltage = 1.0 + (qs_pulse * 0.4) + (mf_pulse * 0.4) + (echo_pulse * 0.3) + (void_pulse * 0.2)
        
        for step in (seq if seq else [[0.1, 0.1, 0.1, 0.1, inertia]]):
            interference = (1.0 + unified * 0.1) * (1.0 + inertia * 0.08) * pulse_voltage
            if BRIAN2_AVAILABLE:
                self.neurons.I_in = step[0] * step[1] * self.gain * topo_array * interference
                self.net.run(5 * b2.ms, namespace={})
                voltages, haptic_level = np.array(self.neurons.v[:]), np.mean(self.neurons.haptic_fb[:])
            else:
                voltages = np.clip(topo_array * interference * step[0] * 0.8, 0, 1.2)
                haptic_level = np.mean(voltages) * 0.2
        
        self.gain = np.clip(self.gain + (0.45 - np.mean(voltages)) * 0.1, 0.1, 5.0)
        avg_coh, avg_sync = (np.mean([s[0] for s in seq]), np.mean([s[1] for s in seq])) if seq else (0.5, 0.5)
        
        # Backward compatibility layer: pass raw_file_path to observers that support **kwargs
        scores = {k: obs.evaluate(avg_coh, avg_sync, unified, voltages, text=parsed_txt, haptic_level=haptic_level, mod=mod, file_path=file_path) for k, obs in self.observers.items()}
        gov_mode, conf = self.governor.select_governor(scores, unified)
        
        return voltages, unified, gov_mode, scores, haptic_level, inertia, mod, core_phases, qs_pulse, mf_pulse, echo_pulse, void_pulse

# ──────────────────────────────────────────────────────────────────────
# 5. MULTIMODAL SUBCONSCIOUS GENERATOR (SWARM / QWEN)
# ──────────────────────────────────────────────────────────────────────
class MultimodalSubconsciousSwarm:
    def __init__(self):
        self.use_transformers = TRANSFORMERS_AVAILABLE
        self.current_model_name = "facebook/opt-125m" # Default text fallback
        self.model = None
        self.processor = None
        self.is_multimodal = False
        self.device = "cpu" # Forced CPU for Latitude 5420
        self.dtype = torch.bfloat16 # Reduced precision to save RAM
        
        if self.use_transformers: 
            self.switch_model(self.current_model_name)
            
        self.semantic_seeds = {
            "OMN": ["Processing omnipotent layer,"], 
            "GRK": ["As Grok, I observe that", "Truth-seeking mode engaged:"],
            "STR": ["Orbital telemetry aligns with the current node,"], 
            "VIS": ["The visual graph indicates that"],
            "CQA": ["Quantum entanglement observed in input stream,"], 
            "CLS": ["Gradient error decaying optimally,"]
        }
        self.context_memory = "System initialized safely."
        self.fallback_seeds = ["Enter Signal", "Initiate scan", "No error detected"]

    def purge(self):
        """Aggressive RAM clearing before loading heavy models."""
        if self.model is not None:
            del self.model
            if self.processor is not None:
                del self.processor
            self.model = None
            self.processor = None
        import gc
        gc.collect()

    def switch_model(self, model_name):
        model_name = model_name.strip(" []'\"")
        if model_name.endswith(('.pt', '.pth')): return False
        if not self.use_transformers: return False
        
        self.purge() # Clear RAM to prevent OOM on 16GB system
        
        try:
            print(f"\n 🔄 Switching Subconscious Generator to: [{model_name}] (CPU bfloat16)...")
            if "qwen2-vl" in model_name.lower():
                self.processor = AutoProcessor.from_pretrained(model_name)
                self.model = Qwen2VLForConditionalGeneration.from_pretrained(
                    model_name, 
                    torch_dtype=self.dtype,
                    low_cpu_mem_usage=True # Crucial for 16GB RAM limits
                ).to(self.device).eval()
                self.is_multimodal = True
                self.tokenizer = self.processor.tokenizer
            else:
                self.tokenizer = AutoTokenizer.from_pretrained(model_name)
                if getattr(self.tokenizer, 'pad_token', None) is None: 
                    self.tokenizer.pad_token = self.tokenizer.eos_token
                self.model = AutoModelForCausalLM.from_pretrained(
                    model_name, 
                    torch_dtype=self.dtype,
                    low_cpu_mem_usage=True
                ).to(self.device).eval()
                self.is_multimodal = False
                
            self.current_model_name = model_name
            print("   ✅ Model switch successful.")
            return True
        except Exception as e: 
            print(f"   ❌ Switch Failed: {e}")
            self.purge()
            return False

    def generate_signal(self, current_gov="OMN", haptic_val=0.0, last_file=None):
        if not self.use_transformers or self.model is None: 
            return random.choice(self.fallback_seeds)
            
        seed_list = self.semantic_seeds.get(current_gov, [f"System evaluating under {current_gov} matrix node,"])
        theme = random.choice(seed_list)
        
        try:
            if self.is_multimodal and last_file and last_file.endswith(('.png', '.jpg', '.jpeg')):
                img = Image.open(last_file).convert("RGB").resize((224, 224))
                messages = [
                    {"role": "user", "content": [
                        {"type": "image", "image": img},
                        {"type": "text", "text": f"{self.context_memory[-80:]}\n[State: {current_gov}] {theme}"}
                    ]}
                ]
                text_prompt = self.processor.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
                inputs = self.processor(text=[text_prompt], images=[img], return_tensors="pt").to(self.device)
                
                with torch.no_grad():
                    output_ids = self.model.generate(**inputs, max_new_tokens=15)
                    generated_ids_trimmed = [
                        out_ids[len(in_ids):] if len(out_ids) > len(in_ids) else out_ids
                        for in_ids, out_ids in zip(inputs.input_ids, output_ids)
                    ]
                    new_signal = self.processor.batch_decode(generated_ids_trimmed, skip_special_tokens=True)[0].strip()
            else:
                input_ids = self.tokenizer.encode(f"{self.context_memory[-80:]}\n[State: {current_gov}] {theme}", return_tensors="pt").to(self.device)
                with torch.no_grad():
                    output_ids = self.model.generate(
                        input_ids, max_new_tokens=15, do_sample=True, temperature=0.65, top_p=0.80, 
                        repetition_penalty=1.2, pad_token_id=self.tokenizer.pad_token_id, eos_token_id=self.tokenizer.eos_token_id
                    )
                if output_ids.size(0) > 0 and input_ids.size(1) < output_ids.size(1):
                    new_signal = re.sub(r'\[\d+\]|^[,\.\s]+', '', self.tokenizer.decode(output_ids[0][len(input_ids[0]):], skip_special_tokens=True).strip())
                else:
                    new_signal = theme + " stable."
                    
        except Exception as e:
            new_signal = theme + " operational variance."

        if len(new_signal) < 3: 
            new_signal = theme + " stable."
            
        self.context_memory = (self.context_memory + " " + new_signal)[-200:]
        return new_signal

# ──────────────────────────────────────────────────────────────────────
# 6. CLI ENGINE
# ──────────────────────────────────────────────────────────────────────
def start():
    print("\n" + "💠"*35)
    print(" 🚀 HOLOSYN ULTIMATE V5.8: MULTIMODAL OMNI-RESONANCE")
    print("💠"*35)
    print(" COMMANDS:")
    print("   [Text/URL/File]    : Analyze Text, scrape Web, or ingest local Image/Audio/Doc")
    print("   /model [Name]      : Switch Subconscious (Supports Qwen2-VL!)")
    print("   /add [Name/File]   : Clone Foundation for Concept, URL, or File")
    print("   /plugin [Path/URL] : Inject .py Observers OR .pt Core weights (Comma-separated for multiple)")
    print("   /vault [Path/URL]  : Harvest .pt weights AND .py plugins from folder")
    print("   /pulse [Value]     : Manually override feedback pulse intensity")
    print("   /auto              : Toggle autonomous generator")
    print("─"*70)
    
    nexus = HolosynDynamic(".")
    subconscious = MultimodalSubconsciousSwarm()
    auto_mode, last_gov, last_haptic = False, "OMN", 0.0

    while True:
        try:
            if not auto_mode:
                cmd = input("\n[OMNI SIGNAL] > ").strip()
                if not cmd: break
                parts = cmd.split(" ", 1)
                cmd_base, cmd_arg = parts[0], parts[1] if len(parts) > 1 else ""
                
                if cmd_base == "/auto":
                    auto_mode = True
                    print("\n 🌀 AUTONOMOUS SUBCONSCIOUS ENGAGED...")
                    time.sleep(1.0)
                    continue
                elif cmd_base == "/model": 
                    subconscious.switch_model(cmd_arg or "facebook/opt-125m")
                    continue
                elif cmd_base == "/vault": 
                    nexus.rebuild_manifold(cmd_arg or ".")
                    continue
                elif cmd_base == "/plugin": 
                    # UPDATED: Support for comma-separated plugin installation
                    plugins_to_load = [p.strip() for p in cmd_arg.split(',') if p.strip()]
                    for p in plugins_to_load:
                        nexus.load_plugin(p)
                    continue
                elif cmd_base == "/add":
                    target = cmd_arg
                    if not target:
                        print("\n   [NEXUS]: Enter Concept, File Path, or URL:")
                        target = input("   > ").strip()
                    if target: 
                        nexus.add_core(target)
                    else: 
                        print("   ❌ Core addition cancelled.")
                    continue
                elif cmd_base == "/pulse":
                    try: 
                        nexus.pulse_override = float(cmd_arg)
                        print(f" 🎛️ OVERRIDE: {nexus.pulse_override}")
                    except: 
                        nexus.pulse_override = None
                        print(" 🎛️ OVERRIDE DISABLED.")
                    continue
                elif cmd_base == "/grok": 
                    last_gov = "GRK"
                    print("🧠 GROK GOVERNOR FORCED")
                    continue
            else:
                # Passes last_file_path for multimodal hallucinations
                cmd = subconscious.generate_signal(current_gov=last_gov, haptic_val=last_haptic, last_file=nexus.last_file_path)
                print(f"\n[SUBCONSCIOUS INJECT]: {cmd}")
                time.sleep(1.5)

            if cmd.startswith('/'): continue

            v, uni, gov, scores, haptic, inertia, mod, core_phases, qs_pulse, mf_pulse, echo_pulse, void_pulse = nexus.process(cmd)
            last_gov, last_haptic = gov, haptic

            print("═"*70)
            print(f" 📡 {mod} | ⏳ INERTIA: {inertia:.3f} | 🌀 UNIFIED PHASE: {uni:.5f}")
            print(f" 🧠 CORE GOVERNOR : {gov} | 💓 MULTIMODAL PULSE : {haptic:.4f}")
            print("─" * 70)
            
            core_str = " | ".join([f"🥃 {k}: {v:.4f}" for k, v in list(core_phases.items())[:8]])
            if len(core_phases) > 8: 
                core_str += f" ... (+{len(core_phases)-8} more)"
            print(f" 🧬 ACTIVE CORES: {core_str}")
            print(f" ⚡ PULSE SIGNATURES: [Q-Star: {qs_pulse:.4f} | Manifold: {mf_pulse:.4f} | Echo: {echo_pulse:.4f} | Void: {void_pulse:.4f}]")
            
            matrix = " | ".join([f"{k}: {v:.2f}" for k, v in list(scores.items())[:12]])
            if len(scores) > 12: 
                matrix += f" ... (+{len(scores)-12})"
            print(f" ⚖️ CONSENSUS: [{matrix}]")
            print("─" * 70)
            
            for name, volt in zip(nexus.topology.keys(), v):
                print(f" {name:>12} : {'█' * int(max(0, volt * 20))} ({volt:.2f})")
            print("═"*70)

        except KeyboardInterrupt:
            if auto_mode: 
                auto_mode = False
                print("\n 🛑 AUTONOMOUS SUBCONSCIOUS HALTED.")
            else: break
        except Exception as e: 
            import traceback
            print(f"❌ Core Fault: {e}")
            traceback.print_exc()
            if auto_mode:
                auto_mode = False
                print("🛑 Halting auto-loop due to fault.")

if __name__ == "__main__":
    start()