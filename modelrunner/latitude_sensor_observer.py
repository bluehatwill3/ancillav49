#!/usr/bin/env python3
"""
HOLOSYN V5.8: DELL LATITUDE SENSOR ARRAY
================================================================
Hardware: Dell Latitude 5420 (i5-1145G7)
Role: Background Environmental Polling (Camera, Mic, Wireless)
Architecture: Asynchronous Daemon Threads to prevent main-loop blocking.
"""

import os
import time
import threading
import subprocess
import numpy as np
import warnings

# Suppress ALSA/Audio backend warnings common on Linux/Windows
warnings.filterwarnings("ignore")

# Dynamic Compatibility Bridge
try:
    from __main__ import BaseObserver
except ImportError:
    class BaseObserver:
        def evaluate(self, s, sy, p, snn, text="", haptic_level=0.0, **kwargs): return 0.5

# Hardware Library Imports
try:
    import cv2
    CV2_AVAILABLE = True
except ImportError:
    CV2_AVAILABLE = False

try:
    import sounddevice as sd
    AUDIO_AVAILABLE = True
except ImportError:
    AUDIO_AVAILABLE = False


class LatitudeSensorObserver(BaseObserver):
    def __init__(self):
        super().__init__()
        self.device_name = "Dell Latitude 5420"
        
        # Real-time Sensory Buffers
        self.ambient_brightness = 0.5
        self.optical_flow = 0.0
        self.ambient_volume = 0.0
        self.wireless_entropy = 0.5
        
        # Hardware limits and flags
        self.running = True
        
        print(f"📡 [HARDWARE ARRAY] Initializing physical sensors for {self.device_name}...")
        
        # Start Asynchronous Sensor Threads
        if CV2_AVAILABLE:
            threading.Thread(target=self._poll_camera, daemon=True).start()
        else:
            print("   ⚠️ [CAMERA] OpenCV not found. Optical parsing disabled.")
            
        if AUDIO_AVAILABLE:
            threading.Thread(target=self._poll_audio, daemon=True).start()
        else:
            print("   ⚠️ [AUDIO] SoundDevice not found. Acoustic parsing disabled.")
            
        threading.Thread(target=self._poll_wireless, daemon=True).start()

    def _poll_camera(self):
        """Background thread: Captures webcam data to detect motion and light."""
        # Index 0 is standard for the Latitude's integrated webcam
        cap = cv2.VideoCapture(0)
        
        # Lower resolution to save i5 CPU cycles
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)
        
        last_frame = None
        
        while self.running:
            ret, frame = cap.read()
            if ret:
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                
                # 1. Calculate Ambient Light (0.0 to 1.0)
                self.ambient_brightness = np.mean(gray) / 255.0
                
                # 2. Calculate Optical Flow / Motion (0.0 to 1.0)
                if last_frame is not None:
                    diff = cv2.absdiff(last_frame, gray)
                    motion = np.mean(diff)
                    self.optical_flow = np.clip(motion / 50.0, 0.0, 1.0)
                    
                last_frame = gray
            time.sleep(0.1) # 10 FPS is plenty for ambient tracking
            
        cap.release()

    def _poll_audio(self):
        """Background thread: Captures microphone RMS (volume) level."""
        def audio_callback(indata, frames, time_info, status):
            if status:
                pass # Ignore buffer under/overflows
            # Calculate RMS (Root Mean Square) volume
            rms = np.sqrt(np.mean(indata**2))
            # Scale to roughly 0.0 - 1.0 based on typical laptop mic gain
            self.ambient_volume = np.clip(rms * 10.0, 0.0, 1.0)

        try:
            # Standard Latitude integrated mic: 1 channel, 16kHz
            with sd.InputStream(callback=audio_callback, channels=1, samplerate=16000):
                while self.running:
                    time.sleep(0.5)
        except Exception as e:
            print(f"   ⚠️ [AUDIO FAULT] Mic locked by OS: {e}")

    def _poll_wireless(self):
        """Background thread: Scans Wi-Fi networks to gauge environmental entropy."""
        while self.running:
            try:
                # Cross-platform check for nearby networks
                if os.name == 'nt': # Windows
                    output = subprocess.check_output(['netsh', 'wlan', 'show', 'networks'], stderr=subprocess.STDOUT, text=True)
                    network_count = output.count("SSID")
                else: # Linux/Ubuntu
                    output = subprocess.check_output(['nmcli', '-t', '-f', 'SSID', 'dev', 'wifi'], stderr=subprocess.STDOUT, text=True)
                    network_count = len([x for x in output.split('\n') if x])
                
                # More networks = higher environmental interference/entropy
                self.wireless_entropy = np.clip(network_count / 20.0, 0.1, 1.0)
            except Exception:
                self.wireless_entropy = 0.5
                
            time.sleep(10) # Only scan every 10 seconds to save battery and network card

    def evaluate(self, s, sy, p, snn, text="", haptic_level=0.0, **kwargs):
        """
        Merges physical reality with the Holosyn cognitive state.
        """
        # 1. Synthesize Physical State
        physical_entropy = (self.optical_flow * 0.4) + (self.ambient_volume * 0.4) + (self.wireless_entropy * 0.2)
        
        # 2. Inject into kwargs for the Agentic Swarm & Pulse Mechanics
        # The Swarm Observer can now 'see' the physical world data
        kwargs['physical_brightness'] = self.ambient_brightness
        kwargs['physical_motion'] = self.optical_flow
        kwargs['physical_volume'] = self.ambient_volume
        kwargs['wireless_entropy'] = self.wireless_entropy
        
        # 3. Alter system resonance based on the physical environment
        # If the room is loud and chaotic, sync drops. If quiet, sync increases.
        environmental_impact = 1.0 - physical_entropy
        
        final_resonance = np.clip((s * 0.4) + (sy * 0.4 * environmental_impact) + (p * 0.2), 0.0, 1.0)
        
        return float(final_resonance)