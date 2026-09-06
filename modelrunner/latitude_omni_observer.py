#!/usr/bin/env python3
"""
HOLOSYN V5.8: DELL LATITUDE 5420 OMNI-ENVIRONMENT EMBEDDED MATRIX
===================================================================
Hardware Signature: Dell Latitude 5420 (i5-1145G7 | 16GB RAM | Intel Iris Xe)
Target Node: Low-overhead System Telemetry & Asynchronous Hardware Hooks
Guards: Non-blocking execution loops, fault isolation, self-healing camera threads.
"""

import os
import sys
import time
import threading
import subprocess
import numpy as np
import warnings

# Suppress verbose system backend telemetry
warnings.filterwarnings("ignore")

# ──────────────────────────────────────────────────────────────────────
# 🔌 COGNITIVE RUNTIME INTEGRATION BRIDGE
# ──────────────────────────────────────────────────────────────────────
try:
    from __main__ import BaseObserver
except ImportError:
    class BaseObserver:
        def evaluate(self, s, sy, p, snn, text="", haptic_level=0.0, **kwargs): 
            return 0.5

# Advanced Hardware Library Validation
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

try:
    import psutil
    PSUTIL_AVAILABLE = True
except ImportError:
    PSUTIL_AVAILABLE = False


class LatitudeOmniObserver(BaseObserver):
    def __init__(self):
        super().__init__()
        self.device_name = "Dell Latitude 5420 (i5-1145G7)"
        self.running = True
        
        # ────────── Real-Time Hardware Telemetry Buffers ──────────
        self.ambient_brightness = 0.5
        self.optical_flow = 0.0
        self.ambient_volume = 0.0
        
        # System & Compute Environment
        self.cpu_usage = 0.0
        self.ram_usage = 0.0
        self.core_temperature = 45.0  # Celsius baseline
        
        # Hard Drive Telemetry
        self.disk_free_gb = 0.0
        self.disk_percent_used = 0.0
        self.disk_io_entropy = 0.0
        self.last_disk_rw = 0
        
        # Wireless & Local Connectivity
        self.wireless_entropy = 0.5
        self.bluetooth_active = False
        self.bluetooth_device_count = 0

        print(f"📡 [HARDWARE INITIALIZE] Aligning subsystems for {self.device_name}...")

        # ────────── Thread Allocation Matrix ──────────
        # Spawning independent daemon tasks to ensure zero lag on the i5 CPU
        threading.Thread(target=self._poll_camera_loop, daemon=True).start()
        
        if AUDIO_AVAILABLE:
            threading.Thread(target=self._poll_audio_loop, daemon=True).start()
        else:
            print("   ⚠️ [AUDIO] 'sounddevice' module unavailable. Acoustic parsing suspended.")

        if PSUTIL_AVAILABLE:
            threading.Thread(target=self._poll_compute_and_disk, daemon=True).start()
        else:
            print("   ⚠️ [SYSTEM] 'psutil' module unavailable. Disk and hardware environment tracking restricted.")

        threading.Thread(target=self._poll_connectivity_loop, daemon=True).start()

    # ──────────────────────────────────────────────────────────────────────
    # 📷 SELF-HEALING OPTICAL CORES (Fixes the V4L2 Device Lock Defect)
    # ──────────────────────────────────────────────────────────────────────
    def _poll_camera_loop(self):
        """Asynchronously cycles through hardware addresses. If locked, it safely back-steps instead of crashing."""
        if not CV2_AVAILABLE:
            print("   ⚠️ [CAMERA] OpenCV missing. Optical parsing offline.")
            return

        last_frame = None
        
        while self.running:
            cap = None
            # Target media nodes discovered via system mapping (0 and 2 are standard RGB/IR)
            for index in [0, 2, 1, 3]:
                try:
                    # Injecting explicit Linux V4L2 structures
                    temp_cap = cv2.VideoCapture(index, cv2.CAP_V4L2)
                    if temp_cap.isOpened():
                        # Configure strict resource limitations for the Iris Xe pipeline
                        temp_cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))
                        temp_cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
                        temp_cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)
                        
                        time.sleep(0.2)  # Give driver room to negotiate hardware bounds
                        ret, frame = temp_cap.read()
                        if ret and frame is not None:
                            cap = temp_cap
                            print(f"   ✅ [CAMERA-NODE] Bind successful on link index: /dev/video{index}")
                            break
                        temp_cap.release()
                except Exception:
                    continue

            if cap is None:
                # FAULT PROTECTION: If camera is locked by web browsers/system apps, update indicators gracefully
                self.optical_flow = 0.0
                self.ambient_brightness = 0.5
                # Cooling loop: Wait 30 seconds before attempting another hardware handshake
                time.sleep(30)
                continue

            # Active frame capture loop
            while self.running:
                try:
                    ret, frame = cap.read()
                    if not ret or frame is None:
                        print("   ⚠️ [CAMERA-NODE] Hardware connection dropped. Resetting channel pipeline...")
                        break
                    
                    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                    self.ambient_brightness = float(np.mean(gray) / 255.0)

                    if last_frame is not None:
                        diff = cv2.absdiff(last_frame, gray)
                        motion = np.mean(diff)
                        # Throttle output metrics into strict float normalization maps
                        self.optical_flow = float(np.clip(motion / 40.0, 0.0, 1.0))

                    last_frame = gray
                    time.sleep(0.2)  # Keep collection capped at ~5 FPS to save battery and computing metrics
                except Exception:
                    break

            cap.release()
            time.sleep(2)

    # ──────────────────────────────────────────────────────────────────────
    # 🎙️ ACOUSTIC POLL CORE
    # ──────────────────────────────────────────────────────────────────────
    def _poll_audio_loop(self):
        """Monitors microphone Root Mean Square (RMS) volume without holding thread locks."""
        def audio_callback(indata, frames, time_info, status):
            if status:
                return
            rms = np.sqrt(np.mean(indata**2))
            self.ambient_volume = float(np.clip(rms * 12.0, 0.0, 1.0))

        try:
            # Low footprint configuration: 16kHz Mono audio block mapping
            with sd.InputStream(callback=audio_callback, channels=1, samplerate=16000, blocksize=2048):
                while self.running:
                    time.sleep(1)
        except Exception:
            print("   ⚠️ [AUDIO-LOCK] System microphone locked by desktop host server or active audio layer.")
            self.ambient_volume = 0.0

    # ──────────────────────────────────────────────────────────────────────
    # 💾 STORAGE ENGINE & COMPUTER ENVIRONMENT TELEMETRY
    # ──────────────────────────────────────────────────────────────────────
    def _poll_compute_and_disk(self):
        """Scrapes CPU core temperatures, usage maps, and storage matrix metrics."""
        while self.running:
            try:
                # Compute usage arrays
                self.cpu_usage = float(psutil.cpu_percent(interval=None) / 100.0)
                self.ram_usage = float(psutil.virtual_memory().percent / 100.0)

                # Fetch internal CPU thermal sensors (Intel coretemp)
                temps = psutil.sensors_temperatures()
                if 'coretemp' in temps and len(temps['coretemp']) > 0:
                    self.core_temperature = float(temps['coretemp'][0].current)
                elif 'cpu_thermal' in temps and len(temps['cpu_thermal']) > 0:
                    self.core_temperature = float(temps['cpu_thermal'][0].current)
                else:
                    self.core_temperature = 45.0 # Hardware baseline configuration

                # Hard drive analytics
                disk_info = psutil.disk_usage('/')
                self.disk_free_gb = float(disk_info.free / (1024**3))
                self.disk_percent_used = float(disk_info.percent / 100.0)

                # Calculate drive read/write IO delta to gauge systemic data processing entropy
                io_counters = psutil.disk_io_counters()
                if io_counters:
                    current_rw_total = io_counters.read_bytes + io_counters.write_bytes
                    if self.last_disk_rw > 0:
                        delta = current_rw_total - self.last_disk_rw
                        # Scale to metric between 0.0 and 1.0 representing disk strain
                        self.disk_io_entropy = float(np.clip(delta / (50 * 1024 * 1024), 0.0, 1.0))
                    self.last_disk_rw = current_rw_total

            except Exception:
                pass
            time.sleep(3.0)  # Throttled parsing loop maps beautifully to the i5 processor footprint

    # ──────────────────────────────────────────────────────────────────────
    # 📶 BLUETOOTH & WIRELESS NETWORK MATRIX
    # ──────────────────────────────────────────────────────────────────────
    def _poll_connectivity_loop(self):
        """Queries local Wi-Fi nodes and standard system Bluetooth adapters via raw subprocess hooks."""
        while self.running:
            try:
                # 1. Evaluate Linux Wireless Signatures via nmcli
                if os.path.exists("/usr/bin/nmcli") or os.path.exists("/bin/nmcli"):
                    output = subprocess.check_output(['nmcli', '-t', '-f', 'SSID', 'dev', 'wifi'], 
                                                     stderr=subprocess.DEVNULL, text=True)
                    networks = len([x for x in output.split('\n') if x.strip()])
                    self.wireless_entropy = float(np.clip(networks / 25.0, 0.0, 1.0))
                else:
                    self.wireless_entropy = 0.3

                # 2. Evaluate Linux Bluetooth Infrastructure via bluetoothctl
                if os.path.exists("/usr/bin/bluetoothctl"):
                    # Query active adapter controller status
                    show_out = subprocess.check_output(['bluetoothctl', 'show'], stderr=subprocess.DEVNULL, text=True)
                    self.bluetooth_active = "Powered: yes" in show_out
                    
                    if self.bluetooth_active:
                        # Parse known registered and discovered peripheral devices
                        dev_out = subprocess.check_output(['bluetoothctl', 'devices'], stderr=subprocess.DEVNULL, text=True)
                        devices = len([x for x in dev_out.split('\n') if x.strip()])
                        self.bluetooth_device_count = devices
                else:
                    self.bluetooth_active = False
                    self.bluetooth_device_count = 0

            except Exception:
                pass
            time.sleep(8.0) # Bluetooth/Wi-Fi updates are resource-heavy, process slowly

    # ──────────────────────────────────────────────────────────────────────
    # ⚖️ DYNAMIC EVALUATION CONVERGENCE
    # ──────────────────────────────────────────────────────────────────────
    def evaluate(self, s, sy, p, snn, text="", haptic_level=0.0, **kwargs):
        """
        Processes physical laptop conditions and feeds telemetry variables 
        directly into the core environment loop.
        """
        # Inject precise laptop telemetry directly into the swarm's accessible properties
        kwargs['physical_brightness'] = self.ambient_brightness
        kwargs['physical_motion'] = self.optical_flow
        kwargs['physical_volume'] = self.ambient_volume
        
        kwargs['cpu_utilization'] = self.cpu_usage
        kwargs['ram_utilization'] = self.ram_usage
        kwargs['hardware_temp_celsius'] = self.core_temperature
        
        kwargs['hd_free_space_gb'] = self.disk_free_gb
        kwargs['hd_percent_used'] = self.disk_percent_used
        kwargs['hd_io_entropy'] = self.disk_io_entropy
        
        kwargs['wireless_entropy'] = self.wireless_entropy
        kwargs['bluetooth_state'] = 1.0 if self.bluetooth_active else 0.0
        kwargs['bluetooth_connections'] = self.bluetooth_device_count

        # Synthesize physical system stress vs environmental turbulence
        system_stress = (self.cpu_usage * 0.4) + (self.ram_usage * 0.4) + (self.disk_io_entropy * 0.2)
        environmental_flux = (self.optical_flow * 0.4) + (self.ambient_volume * 0.4) + (self.wireless_entropy * 0.2)

        # Output telemetry log straight to the runtime terminal
        print(f"\n💻 [DELL LATITUDE TELEMETRY] TEMP: {self.core_temperature:.1f}°C | CPU: {self.cpu_usage*100:.1f}% | RAM: {self.ram_usage*100:.1f}%")
        print(f"📁 [STORAGE & COMM] HD FREE: {self.disk_free_gb:.1f}GB | IO ENTROPY: {self.disk_io_entropy:.2f} | BT DEVICES: {self.bluetooth_device_count}")
        print(f"👁️ [SENSORS] BRIGHT: {self.ambient_brightness:.2f} | MOTION: {self.optical_flow:.2f} | SOUND: {self.ambient_volume:.2f}")
        print("─" * 75)

        # Modify core resonance logic based on machine load
        # High computing stress or loud environmental conditions safely normalize system resonance
        mitigation_factor = 1.0 - (system_stress * 0.3 + environmental_flux * 0.2)
        final_resonance = np.clip((s * 0.3) + (sy * 0.4 * mitigation_factor) + (p * 0.3), 0.0, 1.0)

        return float(final_resonance)