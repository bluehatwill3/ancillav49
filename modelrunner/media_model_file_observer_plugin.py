#!/usr/bin/env python3
"""
HOLOSYN PLUGIN: MEDIA & MODEL FILE OBSERVER
================================================================
Role: Universal File Parsing Interface
Capabilities:
- Dynamically parses Neural Models (.pt, .pth) for weight density.
- Analyzes Images (.jpg, .png) for structural contrast/brightness entropy.
- Evaluates Audio/Video files for temporal resonance.
- 100% backwards compatible with Holosyn V5.8.
"""

import os
import sys
import math
import torch
import numpy as np

# Dynamic BaseObserver Resolution (Backwards Compatible)
# Scans memory to inherit from the exact BaseObserver class the engine is currently using.
BaseObserver = None
for module_name in ['__main__', 'nexus', 'core', 'observer', 'main']:
    if module_name in sys.modules:
        mod = sys.modules[module_name]
        if hasattr(mod, 'BaseObserver'):
            BaseObserver = getattr(mod, 'BaseObserver')
            break

if BaseObserver is None:
    class BaseObserver:
        """Fallback interface for standalone execution or offline testing."""
        def evaluate(self, s, sy, p, snn, text="", haptic_level=0.0, **kwargs):
            return 0.5

# Graceful fallbacks for media processing
try:
    from PIL import Image
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False

try:
    import wave
    WAVE_AVAILABLE = True
except ImportError:
    WAVE_AVAILABLE = False


class MediaModelFileObserver(BaseObserver):
    """
    A complete interface for media and model parsing.
    Dynamically analyzes local files and returns a resonance score 
    based on their structural entropy and weight distributions.
    """
    def __init__(self):
        super().__init__()
        print("📁 [FILE OBSERVER] Media & Model Parsing Interface Online.")

    def _parse_model(self, file_path: str) -> float:
        """Parses PyTorch weights to evaluate neural density and sparsity."""
        try:
            # Load strictly to CPU to prevent VRAM spikes and OOM errors
            weights = torch.load(file_path, map_location="cpu", weights_only=True)
            if hasattr(weights, 'state_dict'):
                weights = weights.state_dict()
            
            total_params = 0
            active_params = 0
            
            # Sample the first 10 tensor layers to gauge density/resonance
            for k, v in list(weights.items())[:10]:
                if isinstance(v, torch.Tensor) and v.is_floating_point():
                    total_params += v.numel()
                    # Calculate how many parameters are non-zero/active
                    active_params += (torch.abs(v) > 0.01).sum().item()
            
            density = active_params / max(1, total_params)
            print(f"   🧠 [MODEL PARSER] Evaluated neural density: {density:.4f}")
            return float(np.clip(density * 1.5, 0.0, 1.0))
        except Exception as e:
            print(f"   ⚠️ [MODEL PARSER] Failed to parse {os.path.basename(file_path)}: {e}")
            return 0.5

    def _parse_image(self, file_path: str) -> float:
        """Parses images to calculate brightness and contrast entropy."""
        if not PIL_AVAILABLE: 
            return 0.5
        try:
            img = Image.open(file_path).convert("L")  # Convert to grayscale
            img_data = np.array(img)
            
            # Calculate image contrast (standard deviation of pixel intensities)
            contrast = np.std(img_data) / 255.0
            brightness = np.mean(img_data) / 255.0
            
            print(f"   🖼️ [IMAGE PARSER] Brightness: {brightness:.2f}, Contrast: {contrast:.2f}")
            return float(np.clip((contrast + brightness) / 2.0, 0.0, 1.0))
        except Exception:
            return 0.5

    def _parse_audio_media(self, file_path: str) -> float:
        """Parses audio waveframes or uses file entropy heuristics."""
        if WAVE_AVAILABLE and file_path.endswith('.wav'):
            try:
                with wave.open(file_path, 'rb') as wf:
                    frames = wf.getnframes()
                    rate = wf.getframerate()
                    duration = frames / float(rate)
                    print(f"   🎵 [AUDIO PARSER] Track Duration: {duration:.2f}s")
                    return min(duration / 10.0, 1.0)  # Normalize up to 10 seconds
            except Exception:
                pass
                
        # Fallback size-based resonance for generic media (MP4, MP3, etc.)
        size_mb = os.path.getsize(file_path) / (1024 * 1024)
        print(f"   🎞️ [MEDIA PARSER] File Size Entropy: {size_mb:.2f} MB")
        return float(np.clip(size_mb / 5.0, 0.1, 1.0))

    def evaluate(self, s, sy, p, snn, text="", haptic_level=0.0, **kwargs):
        """Main Holosyn hook. Evaluates the active file and blends it with system state."""
        file_path = kwargs.get('file_path', None)
        
        # If no file is associated with this tick, run passively
        if not file_path or not os.path.exists(file_path):
            return float(np.clip((s * 0.4) + (sy * 0.4) + (np.mean(snn) * 0.2), 0.0, 1.0))
            
        ext = os.path.splitext(file_path)[1].lower()
        media_resonance = 0.5
        
        # Route to the appropriate media parser
        if ext in ['.pt', '.pth', '.bin', '.safetensors']:
            media_resonance = self._parse_model(file_path)
        elif ext in ['.jpg', '.jpeg', '.png', '.bmp']:
            media_resonance = self._parse_image(file_path)
        elif ext in ['.wav', '.mp3', '.m4a', '.flac', '.mp4', '.avi', '.mkv']:
            media_resonance = self._parse_audio_media(file_path)
        else:
            # Generic Document parsing (Size entropy)
            size_kb = os.path.getsize(file_path) / 1024.0
            media_resonance = min(size_kb / 1000.0, 1.0)
            
        # Cross-modal resonance: Blend file structure with system coherence (s) and pulse (p)
        final_resonance = (media_resonance * 0.6) + (s * 0.2) + (abs(p) * 0.2)
        
        # Inject metrics back into kwargs for potential other plugins or the governor
        kwargs['parsed_media_resonance'] = media_resonance
        
        # Update system mode if needed
        kwargs['mod'] = f"{ext.upper()[1:]}_PARSED"
        
        return float(np.clip(final_resonance, 0.0, 1.0))

# Explicit anchor hooks for dynamic Holosyn plugin loader
observer = MediaModelFileObserver()
plugin_observer = observer

# Validation hook for standalone testing
if __name__ == "__main__":
    print("\n💠 Standalone Verification Run 💠")
    # Simulating a file passing into the observer
    test_score = observer.evaluate(
        s=0.80, sy=0.75, p=0.20, snn=[0.3, 0.5], 
        file_path="mock_image.png", text="Testing media parser."
    )
    print(f"Resonance Output: {test_score:.4f}")