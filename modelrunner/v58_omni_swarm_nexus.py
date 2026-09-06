#!/usr/bin/env python3
"""
HOLOSYN V5.8: MASTER OMNI-SWARM NEXUS & ENVIRONMENT SUITE
===================================================================
Hardware Specification: Dell Latitude 5420 (i5-1145G7 | 16GB RAM | Iris Xe)
System Core: CPU-Optimized Neuromorphic Framework Loop
Features: Specialized Neural Core Observers, Memory-Guarded Vault Management,
          and upgraded Multimodal Self-Reflective Telemetry Orchestration.
"""

import os
import sys
import gc
import json
import re
import time
import warnings
import threading
import subprocess
import numpy as np
import torch
import torch.nn as nn

# Suppress system, driver, and download metadata verbosity
warnings.filterwarnings("ignore")
os.environ["TOKENIZERS_PARALLELISM"] = "false"

# ──────────────────────────────────────────────────────────────────────
# 🔌 WORKSPACE COMPATIBILITY BRIDGE
# ──────────────────────────────────────────────────────────────────────
try:
    from __main__ import BaseObserver
except ImportError:
    class BaseObserver:
        """Fallback base framework to allow localized execution outside runtime."""
        def evaluate(self, s, sy, p, snn, text="", haptic_level=0.0, **kwargs): 
            return 0.5

# Advanced Deep Learning Framework Checks
try:
    from transformers import (
        AutoTokenizer, AutoModelForCausalLM,
        Qwen2VLForConditionalGeneration, AutoProcessor,
        WhisperProcessor, WhisperForConditionalGeneration,
        CLIPProcessor, CLIPModel
    )
    HF_TRANSFORMERS_AVAILABLE = True
except ImportError:
    HF_TRANSFORMERS_AVAILABLE = False

try:
    import sounddevice as sd
    AUDIO_HARDWARE_AVAILABLE = True
except ImportError:
    AUDIO_HARDWARE_AVAILABLE = False

try:
    import cv2
    OPENCV_AVAILABLE = True
except ImportError:
    OPENCV_AVAILABLE = False

try:
    import psutil
    PSUTIL_AVAILABLE = True
except ImportError:
    PSUTIL_AVAILABLE = False


# ──────────────────────────────────────────────────────────────────────
# 🗄️ MASTER OMNI-SWARM MANAGER (Guarded Memory Vault Singleton)
# ──────────────────────────────────────────────────────────────────────
class OmniSwarmManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(OmniSwarmManager, cls).__new__(cls)
            cls._instance.device = "cpu"
            cls._instance.dtype = torch.bfloat16 if torch.cuda.is_available() else torch.float32
            
            # Subconscious Model Properties
            cls._instance.active_model_name = None
            cls._instance.model = None
            cls._instance.processor = None
            cls._instance.tokenizer = None
            
            # Compiled Neural Weights Storage Map
            cls._instance.compiled_cores = {}
            
            # Explicit Hardware Whitelist to guard the 16GB RAM boundary
            cls._instance.whitelist = {
                "text_reasoning": "Qwen/Qwen2.5-0.5B-Instruct",
                "upgraded_vision": "Qwen/Qwen2-VL-2B-Instruct",
                "compact_multimodal": "openai/clip-vit-base-patch32",
                "audio_phonetic": "openai/whisper-tiny"
            }
        return cls._instance

    def purge_memory_pool(self):
        """Forces system garbage collection and releases inactive tensors from RAM."""
        if self.model is not None:
            print(f"   🧹 [MEM-VAULT] Unloading processing layer: {self.active_model_name}...")
            self.model = None
            self.processor = None
            self.tokenizer = None
            self.active_model_name = None
        gc.collect()

    def request_model_allocation(self, role_key):
        """Safely loads or switches active models without triggering Out-Of-Memory conditions."""
        if not HF_TRANSFORMERS_AVAILABLE:
            return False
            
        target_model = self.whitelist.get(role_key, None)
        if not target_model:
            print(f"   🛡️ [GUARD] Access denied. '{role_key}' is outside hardware constraints.")
            return False

        if self.active_model_name == target_model:
            return True  # Already cached in memory

        self.purge_memory_pool()
        print(f"   ⏳ [MEM-VAULT] Allocating hardware layers for: {target_model}...")

        try:
            if role_key == "upgraded_vision":
                self.processor = AutoProcessor.from_pretrained(target_model)
                self.model = Qwen2VLForConditionalGeneration.from_pretrained(
                    target_model, torch_dtype=self.dtype
                ).eval()
            elif role_key == "audio_phonetic":
                self.processor = WhisperProcessor.from_pretrained(target_model)
                self.model = WhisperForConditionalGeneration.from_pretrained(
                    target_model, torch_dtype=self.dtype
                ).eval()
            elif role_key == "compact_multimodal":
                self.processor = CLIPProcessor.from_pretrained(target_model)
                self.model = CLIPModel.from_pretrained(target_model, torch_dtype=self.dtype).eval()
            else:  # Text Reasoning Base Loop
                self.tokenizer = AutoTokenizer.from_pretrained(target_model)
                if self.tokenizer.pad_token is None:
                    self.tokenizer.pad_token = self.tokenizer.eos_token
                self.model = AutoModelForCausalLM.from_pretrained(
                    target_model, torch_dtype=self.dtype
                ).eval()

            self.active_model_name = target_model
            print(f"   ✅ [MEM-VAULT] Swap successful. System linked to {target_model}.")
            return True
        except Exception as e:
            print(f"   ❌ [MEM-VAULT] Failed allocation for {target_model}: {e}")
            self.purge_memory_pool()
            return False

    def load_neural_core_weights(self, core_name, path):
        """Registers external .pt weights files cleanly into the internal structure mapping."""
        if os.path.exists(path):
            try:
                # Map to CPU explicitly to accommodate lack of dedicated GPU
                weights = torch.load(path, map_location="cpu")
                self.compiled_cores[core_name] = weights
                print(f"   💾 [CORE-REGISTRY] Hooked structural weights for: {core_name}")
                return True
            except Exception as e:
                print(f"   ⚠️ [CORE-REGISTRY] Handshake bypass for {core_name}: running simulated parameters ({e})")
        return False


# ──────────────────────────────────────────────────────────────────────
# 🎛️ SYSTEM BLUEPRINT ARCHITECTURE
# ──────────────────────────────────────────────────────────────────────
class TransformerCore(nn.Module):
    """The mathematical architecture layout required by the core forge ecosystem."""
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
        seq_len = x.size(1)
        emb = self.embedding(x) + self.pos_encoder[:, :seq_len, : ]
        return torch.tanh(self.projector(self.transformer(emb).mean(dim=1)).squeeze(-1))


# ──────────────────────────────────────────────────────────────────────
# 👁️ SPECIALIZED CORES OBSERVER ARRAY (Task-Specific Automation)
# ──────────────────────────────────────────────────────────────────────

class CryptoEchoChamberObserver(BaseObserver):
    """Parses digital network structures, algorithmic velocity signals, and data trends."""
    def evaluate(self, s, sy, p, snn, text="", haptic_level=0.0, **kwargs):
        manager = OmniSwarmManager()
        velocity = float(np.clip(len(text) / 280.0, 0.0, 1.0)) if text else 0.1
        spike_activity = np.mean(snn) if (snn is not None and len(snn) > 0) else 0.5
        
        # Pull signals from simulated or loaded state dict configurations
        has_weights = "CRYPTO_TWITTER_CORE" in manager.compiled_cores
        bias_modulation = 0.85 if has_weights else 0.50
        
        resonance = np.clip((s * 0.3) + (velocity * 0.4) + (spike_activity * 0.3 * bias_modulation), 0.0, 1.0)
        return float(resonance)


class AcousticManifoldObserver(BaseObserver):
    """Tracks localized resonance fields, auditory envelopes, and raw waveform oscillations."""
    def evaluate(self, s, sy, p, snn, text="", haptic_level=0.0, **kwargs):
        mic_amplitude = kwargs.get('physical_volume', 0.1)
        phase_alignment = math.sin(p) * 0.5 + 0.5
        
        resonance = np.clip((sy * 0.4) + (mic_amplitude * 0.4) + (phase_alignment * 0.2), 0.0, 1.0)
        return float(resonance)


class MarketVolatilityObserver(BaseObserver):
    """Processes computational risk dynamics, entropy distributions, and structural variance."""
    def evaluate(self, s, sy, p, snn, text="", haptic_level=0.0, **kwargs):
        cpu_load = kwargs.get('cpu_utilization', 0.2)
        snn_variance = np.var(snn) if (snn is not None and len(snn) > 0) else 0.05
        
        # Market calculations interpret high system shifts as systemic momentum bursts
        risk_index = np.clip((cpu_load * 0.5) + (snn_variance * 5.0), 0.0, 1.0)
        resonance = np.clip(1.0 - (risk_index - s)**2, 0.0, 1.0)
        return float(resonance)


class GuardianImmuneObserver(BaseObserver):
    """Monitors localized file boundaries, operational permissions, and exception parameters."""
    def evaluate(self, s, sy, p, snn, text="", haptic_level=0.0, **kwargs):
        hd_strain = kwargs.get('hd_io_entropy', 0.1)
        thermal_ceiling = kwargs.get('hardware_temp_celsius', 45.0)
        
        # System defense metrics drop if the core is running dangerously hot
        security_buffer = 1.0 if thermal_ceiling < 82.0 else 0.4
        resonance = np.clip((s * 0.5) + ((1.0 - hd_strain) * 0.5 * security_buffer), 0.0, 1.0)
        return float(resonance)


class OracleProphecyObserver(BaseObserver):
    """Generates future prediction maps and forward context vectors for the swarm model."""
    def evaluate(self, s, sy, p, snn, text="", haptic_level=0.0, **kwargs):
        snn_mean = np.mean(snn) if (snn is not None and len(snn) > 0) else 0.5
        forward_momentum = float(np.clip(s * sy * 1.5, 0.0, 1.0))
        
        resonance = np.clip((forward_momentum * 0.6) + (snn_mean * 0.4), 0.0, 1.0)
        return float(resonance)


class RoboticKinematicsObserver(BaseObserver):
    """Maps haptic metrics, optical frame transitions, and balance/coordination tracking."""
    def evaluate(self, s, sy, p, snn, text="", haptic_level=0.0, **kwargs):
        optical_delta = kwargs.get('physical_motion', 0.0)
        coordination = float(np.clip(1.0 - abs(p - 0.5), 0.0, 1.0))
        
        resonance = np.clip((haptic_level * 0.4) + (optical_delta * 0.3) + (coordination * 0.3), 0.0, 1.0)
        return float(resonance)


class DeepSeekGeoethicsObserver(BaseObserver):
    """Processes global standard frameworks, local compliance rules, and data structures."""
    def evaluate(self, s, sy, p, snn, text="", haptic_level=0.0, **kwargs):
        iso_consensus = np.clip(1.0 - abs(sy - 0.5), 0.0, 1.0)
        snn_density = np.mean(snn) if (snn is not None and len(snn) > 0) else 0.5
        resilience = np.clip(snn_density * 0.6 + haptic_level * 0.4, 0.0, 1.0)
        
        laozi_simplicity = np.clip(1.0 - (len(text) / 1500.0), 0.2, 1.0) if text else 0.6
        ethics_index = (iso_consensus + resilience + laozi_simplicity + p) / 4.0
        return float(np.clip(ethics_index, 0.0, 1.0))


# ──────────────────────────────────────────────────────────────────────
# 🧠 UPGRADED MULTIMODAL SELF-REFLECTIVE COGNITIVE LOOP
# ──────────────────────────────────────────────────────────────────────
class OmniAgenticSwarmObserver(BaseObserver):
    """
    Upgraded Multimodal Self-Reflective Controller. Reads both physical terminal data 
    and systemic context arrays, routing requirements seamlessly while preventing OOM faults.
    """
    def __init__(self):
        super().__init__()
        self.manager = OmniSwarmManager()
        self.history = []
        
        # Hardware Polling State Storage Buffers
        self.ambient_brightness = 0.5
        self.optical_flow = 0.0
        self.ambient_volume = 0.0
        self.cpu_usage = 0.1
        self.ram_usage = 0.3
        self.core_temp = 45.0
        self.disk_entropy = 0.05
        self.disk_free = 100.0
        self.wireless_entropy = 0.3
        
        self.running = True
        
        # Seed core arrays asynchronously to bypass system delay drops
        self._harvest_existing_workspace()
        
        # Fire Hardware Polling Infrastructure Threads
        threading.Thread(target=self._hardware_sensor_polling, daemon=True).start()
        
        # Cache the standard reasoning baseline model to minimize processing startup delays
        self.manager.request_model_allocation("text_reasoning")

    def _harvest_existing_workspace(self):
        """Scrapes standard active directories to discover and bind pre-forged .pt assets."""
        candidate_paths = [
            ("CRYPTO_TWITTER_CORE", "CRYPTO_TWITTER_CORE.pt"),
            ("ACOUSTIC", "acoustic_manifold.pt"),
            ("MARKET_VOLATILITY", "market_vix_qstar.pt"),
            ("IMMUNE_SYSTEM", "GUARDIAN_IMMUNE_CORE.pt"),
            ("ORACLE_PROPHECY", "oracle_prophecy_qstar.pt"),
            ("ROBOTIC_KINEMATICS", "robot_kinematics_manifold.pt")
        ]
        for name, filename in candidate_paths:
            # Check local file positions
            self.manager.load_neural_core_weights(name, filename)

    def _hardware_sensor_polling(self):
        """Asynchronous execution channel extracting metrics without impeding processing cycles."""
        cap = None
        # V4L2 Device Verification Array Loop targeting active pixel channels
        if OPENCV_AVAILABLE:
            for index in [0, 2, 1, 3]:
                try:
                    temp_cap = cv2.VideoCapture(index, cv2.CAP_V4L2)
                    if temp_cap.isOpened():
                        temp_cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))
                        temp_cap.set(cv2.CAP_PROP_FRAME_WIDTH, 160)
                        temp_cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 120)
                        time.sleep(0.1)
                        ret, frame = temp_cap.read()
                        if ret and frame is not None:
                            cap = temp_cap
                            break
                        temp_cap.release()
                except Exception:
                    continue

        last_frame = None
        audio_stream = None
        
        # Sounddevice allocation pipeline block
        audio_buffer = np.zeros((1024, 1))
        if AUDIO_HARDWARE_AVAILABLE:
            try:
                def _audio_chunk_handler(indata, frames, time_info, status):
                    nonlocal audio_buffer
                    if not status:
                        audio_buffer = indata.copy()
                audio_stream = sd.InputStream(callback=_audio_chunk_handler, channels=1, samplerate=16000, blocksize=1024)
                audio_stream.start()
            except Exception:
                audio_stream = None

        while self.running:
            try:
                # 1. Image Metric Analysis Processing
                if cap and cap.isOpened():
                    ret, frame = cap.read()
                    if ret and frame is not None:
                        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                        self.ambient_brightness = float(np.mean(gray) / 255.0)
                        if last_frame is not None:
                            diff = cv2.absdiff(last_frame, gray)
                            self.optical_flow = float(np.clip(np.mean(diff) / 30.0, 0.0, 1.0))
                        last_frame = gray

                # 2. Acoustic Metric Extraction Processing
                if audio_stream:
                    rms = np.sqrt(np.mean(audio_buffer**2))
                    self.ambient_volume = float(np.clip(rms * 15.0, 0.0, 1.0))

                # 3. System Hardware Topology Profiling
                if PSUTIL_AVAILABLE:
                    self.cpu_usage = float(psutil.cpu_percent() / 100.0)
                    self.ram_usage = float(psutil.virtual_memory().percent / 100.0)
                    
                    thermals = psutil.sensors_temperatures()
                    if 'coretemp' in thermals and len(thermals['coretemp']) > 0:
                        self.core_temp = float(thermals['coretemp'][0].current)
                    
                    disk_metrics = psutil.disk_usage('/')
                    self.disk_free = float(disk_metrics.free / (1024**3))
                    self.disk_entropy = float(disk_metrics.percent / 100.0)

                # 4. Wireless Environment Scanning Via Native nmcli
                if os.path.exists("/usr/bin/nmcli") or os.path.exists("/bin/nmcli"):
                    cmd = subprocess.check_output(['nmcli', '-t', '-f', 'SSID', 'dev', 'wifi'], stderr=subprocess.DEVNULL, text=True)
                    count = len([x for x in cmd.split('\n') if x.strip()])
                    self.wireless_entropy = float(np.clip(count / 20.0, 0.0, 1.0))

            except Exception:
                pass
            time.sleep(0.5)

        if cap:
            cap.release()
        if audio_stream:
            audio_stream.stop()

    def build_optimization_prompt(self, s, sy, p, snn_mean, haptic, mod, active_model):
        """Constructs the system state telemetry breakdown block for LLM evaluation."""
        return f"""[SYSTEM TELEMETRY BLOCK]
- Resonance Parameters: S={s:.3f} | SY={sy:.3f} | P={p:.3f}
- Core Activity Vector: SNN_MEAN={snn_mean:.3f} | HAPTIC={haptic:.3f}
- Machine State map: CPU={self.cpu_usage*100:.1f}% | RAM={self.ram_usage*100:.1f}% | THERMAL={self.core_temp:.1f}C
- Storage Matrix: FREE={self.disk_free:.1f}GB | ENTROPY={self.disk_entropy:.2f}
- External Sensors: LUMINANCE={self.ambient_brightness:.2f} | MOTION={self.optical_flow:.2f} | VOLUME={self.ambient_volume:.2f}
- Interface Modality: {mod} | Engine Model Active: {active_model}

TASK:
Analyze parameters and output a precise parameters tuning optimization JSON object matching this structure:
{{
  "gain_multiplier": float (0.1 to 5.0),
  "entropy_injection": float (-0.2 to 0.2),
  "switch_model": string or null ("text_reasoning", "upgraded_vision", "compact_multimodal", "audio_phonetic"),
  "targeted_core": string ("ECHO_CHAMBER", "ACOUSTIC", "MARKET_VOLATILITY", "IMMUNE_SYSTEM", "ORACLE_PROPHECY", "ROBOTIC_KINEMATICS", "GEOETHICS"),
  "summary": string (max 10 words summary statement)
}}
Output ONLY raw JSON code. No markdown tags. No trailing thoughts.
"""

    def evaluate(self, s, sy, p, snn, text="", haptic_level=0.0, **kwargs):
        snn_mean = np.mean(snn) if (snn is not None and len(snn) > 0) else 0.5
        modality_flag = kwargs.get('mod', 'TEXT')
        file_path = kwargs.get('file_path', None)
        
        # --- Context-Driven Modality Pre-Selector ---
        # Explicitly targets upgrades for multimodal assets without breaching memory allocations
        if modality_flag == "IMAGE_NODE" or (file_path and file_path.lower().endswith(('.png', '.jpg', '.jpeg'))):
            self.manager.request_model_allocation("upgraded_vision")
        elif modality_flag == "AUDIO_NODE" or (file_path and file_path.lower().endswith(('.wav', '.mp3'))):
            self.manager.request_model_allocation("audio_phonetic")
            
        current_active = self.manager.active_model_name or "None"
        prompt = self.build_optimization_prompt(s, sy, p, snn_mean, haptic_level, modality_flag, current_active)
        
        suggested_params = {}
        raw_output = ""
        
        # --- Core Execution Engine & Response Parsing Loop ---
        if self.manager.model and hasattr(self.manager, 'tokenizer') and self.manager.active_model_name == self.manager.whitelist["text_reasoning"]:
            try:
                inputs = self.manager.tokenizer(prompt, return_tensors="pt").to(self.manager.device)
                with torch.no_grad():
                    out = self.manager.model.generate(**inputs, max_new_tokens=100, do_sample=False)
                raw_output = self.manager.tokenizer.decode(out[0][inputs.input_ids.size(1):], skip_special_tokens=True).strip()
                
                json_match = re.search(r'\{.*\}', raw_output, re.DOTALL)
                if json_match:
                    suggested_params = json.loads(json_match.group())
            except Exception:
                pass  # Fall back gracefully to computational inertia on parsing failures

        # --- Dynamic Optimization Tuning Conversions ---
        gain = float(np.clip(suggested_params.get('gain_multiplier', 1.0), 0.1, 5.0))
        entropy = float(np.clip(suggested_params.get('entropy_injection', 0.0), -0.2, 0.2))
        target_core_route = suggested_params.get('targeted_core', 'GEOETHICS')
        
        # Inject adjusted parameters directly back into running loop arguments
        kwargs['gain_multiplier'] = gain
        kwargs['entropy_injection'] = entropy
        kwargs['swarm_hallucination'] = suggested_params.get('summary', 'Processing local environmental arrays')
        
        # Inject system metrics maps directly for sister node availability
        kwargs['physical_brightness'] = self.ambient_brightness
        kwargs['physical_motion'] = self.optical_flow
        kwargs['physical_volume'] = self.ambient_volume
        kwargs['cpu_utilization'] = self.cpu_usage
        kwargs['ram_utilization'] = self.ram_usage
        kwargs['hardware_temp_celsius'] = self.core_temp
        kwargs['hd_io_entropy'] = self.disk_entropy
        kwargs['hd_free_space_gb'] = self.disk_free
        kwargs['wireless_entropy'] = self.wireless_entropy

        # --- Model Engine Switching Execution Layer ---
        requested_layer_switch = suggested_params.get('switch_model', None)
        if requested_layer_switch and requested_layer_switch in self.manager.whitelist:
            # Shift model footprint if requested and not running an explicit file lock override
            if modality_flag not in ["IMAGE_NODE", "AUDIO_NODE"]:
                self.manager.request_model_allocation(requested_layer_switch)

        # --- Polymorphic Core Resonance Routing Matrix ---
        # Selects the sub-observer required based on the cognitive swarm's internal evaluation
        if target_core_route == "ECHO_CHAMBER":
            sub_observer = CryptoEchoChamberObserver()
        elif target_core_route == "ACOUSTIC":
            sub_observer = AcousticManifoldObserver()
        elif target_core_route == "MARKET_VOLATILITY":
            sub_observer = MarketVolatilityObserver()
        elif target_core_route == "IMMUNE_SYSTEM":
            sub_observer = GuardianImmuneObserver()
        elif target_core_route == "ORACLE_PROPHECY":
            sub_observer = OracleProphecyObserver()
        elif target_core_route == "ROBOTIC_KINEMATICS":
            sub_observer = RoboticKinematicsObserver()
        else:
            sub_observer = DeepSeekGeoethicsObserver()

        core_resonance = sub_observer.evaluate(s, sy, p, snn, text, haptic_level, **kwargs)
        
        # Console Telemetry Manifest Output Loop
        print(f"\n⚡ [OMNI-SWARM CONTINUUM] Active Core: {target_core_route} | System Resonance: {core_resonance:.4f}")
        print(f"   ⚙️ Optimization Matrix -> Gain Multiplier: {gain:.2f} | Entropy Injection: {entropy:+.2f}")
        print(f"   💬 Cognitive Advisory Summary: \"{kwargs['swarm_hallucination']}\"")
        print("═" * 85)

        final_score = np.clip((core_resonance * 0.7) + (s * 0.3 * gain) + entropy, 0.0, 1.0)
        return float(final_score)


# ──────────────────────────────────────────────────────────────────────
# 🚀 PLUGIN STANDALONE VERIFICATION HOOK
# ──────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("💠 INITIALIZING MASTER OMNI-SWARM NEXUS ENGINE DIRECTORY TRIAL 💠")
    
    # Instantiate Master Controller System
    orchestrator = OmniAgenticSwarmObserver()
    
    # Generate mock sensory tensor representations
    mock_snn_array = np.array([0.12, 0.64, 0.33, 0.81, 0.45])
    
    # Initial testing handshake evaluate execution call
    test_result = orchestrator.evaluate(
        s=0.70, sy=0.75, p=0.40, snn=mock_snn_array, 
        text="Sample neural processing packet input test metrics stream.", 
        haptic_level=0.25, mod="TEXT"
    )