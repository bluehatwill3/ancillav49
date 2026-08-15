import sys
import os
import socket
import threading
import queue
import json
import numpy as np

# ──────────────────────────────────────────────────────────────────────
# 🔌 INTER-MODULE NAMESPACE BRIDGE
# ──────────────────────────────────────────────────────────────────────
# This dynamic hook ensures the plugin inherits from the exact 
# BaseObserver class active in Holosyn's main memory space.
BaseObserver = None
avenues = ['__main__', 'nexus', 'core', 'observer', 'main', 'harvest_manager']
for module_name in avenues:
    if module_name in sys.modules:
        mod = sys.modules[module_name]
        if hasattr(mod, 'BaseObserver'):
            BaseObserver = getattr(mod, 'BaseObserver')
            break

if BaseObserver is None:
    class BaseObserver:
        def evaluate(self, s, sy, p, snn, text="", haptic_level=0.0, **kwargs): 
            return 0.5

# ──────────────────────────────────────────────────────────────────────
# 📡 NETWORK CLI BRIDGE OBSERVER
# ──────────────────────────────────────────────────────────────────────
class NetworkCliBridgeObserver(BaseObserver):
    """
    Holosyn V92: Offsite Network Listener & Interactive CLI Bridge Observer.
    Exposes an asynchronous listening port to safely intercept system telemetry
    and execute dynamic phase overrides via a localized command queue.
    """
    def __init__(self, host="127.0.0.1", port=9999):
        super().__init__()
        self.host = host
        self.port = port
        self.command_queue = queue.Queue()
        self.is_running = True
        
        # Internal state modifiers
        self.bias_modifier = 0.0
        self.phase_modifier = 0.0
        
        # Spin up the background network daemon thread
        self.listener_thread = threading.Thread(target=self._network_listener_loop, daemon=True)
        self.listener_thread.start()
        print(f"   📡 [NETWORK OBSERVER] Background listener initialized on {self.host}:{self.port}")

    def _network_listener_loop(self):
        """Runs a safe, non-blocking background socket server to process offsite tokens."""
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            server_socket.bind((self.host, self.port))
            server_socket.listen(5)
            server_socket.settimeout(1.0)
        except Exception as e:
            print(f"   ❌ [NETWORK ERROR] Failed to bind server socket: {e}")
            return

        while self.is_running:
            try:
                client_socket, addr = server_socket.accept()
                client_socket.settimeout(2.0)
                data = client_socket.recv(1024).decode('utf-8')
                if data:
                    try:
                        # Expects JSON data format: {"bias_mod": 0.1, "phase_mod": -0.2}
                        payload = json.loads(data)
                        self.command_queue.put(payload)
                        client_socket.send(b'{"status": "manifold_accepted"}\n')
                    except json.JSONDecodeError:
                        client_socket.send(b'{"status": "malformed_json_rejected"}\n')
                client_socket.close()
            except socket.timeout:
                continue
            except Exception:
                pass
        server_socket.close()

    def evaluate(self, s, sy, p, snn, text="", haptic_level=0.0, **kwargs):
        """
        Intercepts standard pipeline variables and updates system matrices
        based on active elements within the thread-safe remote loop command queue.
        """
        # Process any pending network commands
        while not self.command_queue.empty():
            try:
                command = self.command_queue.get_nowait()
                self.bias_modifier = float(command.get("bias_mod", self.bias_modifier))
                self.phase_modifier = float(command.get("phase_mod", self.phase_modifier))
                print(f"   ⚡ [OFFSITE OVERRIDE LOGGED] Bias Shift: {self.bias_modifier:+.3f} | Phase Shift: {self.phase_modifier:+.3f}")
            except queue.Empty:
                break

        # Apply target modifications safely to system configurations
        effective_sy = np.clip(sy + self.bias_modifier, 0.0, 1.0)
        effective_p = np.clip(p + self.phase_modifier, -1.0, 1.0)
        
        # Calculate localized system resonance using modified attributes
        base_resonance = (s * 0.4) + (effective_sy * 0.3) + (abs(effective_p) * 0.3)
        final_signal = float(np.clip(base_resonance - (haptic_level * 0.1), 0.0, 1.0))
        
        return final_signal

    def shutdown(self):
        """Gracefully terminates the background network socket daemon."""
        self.is_running = False
        print("   🛑 [NETWORK OBSERVER] System shutdown sequence complete.")