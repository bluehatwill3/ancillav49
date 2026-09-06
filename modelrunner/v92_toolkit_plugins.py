import threading
import socket
import json
import queue
import math
import numpy as np

# Ensure BaseObserver is defined to allow standalone testing
if 'BaseObserver' not in globals():
    class BaseObserver:
        def evaluate(self, s, sy, p, snn, text="", haptic_level=0.0, **kwargs): 
            return 0.5

# ---------------------------------------------------------
# 1. COMPONENT MITIGATION OBSERVER
# ---------------------------------------------------------
class ComponentMitigationObserver(BaseObserver):
    """
    Monitors the availability of core components (Quantum/Neuromorphic) 
    and provides mathematical fallbacks to ensure the system remains stable 
    if a module goes offline or is missing.
    """
    def __init__(self):
        super().__init__()
        # Retrieve global availability flags from the main Holosyn runner
        self.modules = {
            "quantum": globals().get("CIRQ_AVAILABLE", False),
            "neuro": globals().get("BRIAN2_AVAILABLE", False)
        }

    def evaluate(self, s, sy, p, snn, text="", haptic_level=0.0, **kwargs):
        health_score = 1.0
        compensation = 0.0

        # If the quantum engine is missing, simulate quantum interference using a sine wave
        if not self.modules["quantum"]:
            health_score -= 0.2
            compensation += abs(math.sin(p * math.pi) * 0.3)

        # If the neuromorphic engine is missing, use the standard deviation of the array
        if not self.modules["neuro"]:
            health_score -= 0.2
            compensation += (np.std(snn) if len(snn) > 0 else 0.0) * 0.3

        # Blend the actual system coherence with our simulated compensations
        return np.clip((s * health_score) + compensation, 0.0, 1.0)


# ---------------------------------------------------------
# 2. OFFSITE NETWORK & CLI CONTROL OBSERVER
# ---------------------------------------------------------
class NetworkControlObserver(BaseObserver):
    """
    Opens a background socket to receive offsite network commands.
    Allows for real-time prompting and telemetry overrides via CLI or remote connection.
    """
    def __init__(self, host="127.0.0.1", port=9999):
        super().__init__()
        self.host = host
        self.port = port
        self.command_queue = queue.Queue()
        
        # Internal state modifiers that can be changed remotely
        self.active_phase_shift = 0.0
        self.active_bias_shift = 0.0
        
        # Start the background listener thread so it doesn't block the main program
        self.listener_thread = threading.Thread(target=self._listen, daemon=True)
        self.listener_thread.start()
        print(f"📡 [NETWORK OBSERVER] Listening for offsite prompts on {self.host}:{self.port}")

    def _listen(self):
        """Runs a safe background socket server to process incoming JSON tokens."""
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            server.bind((self.host, self.port))
            server.listen(5)
        except Exception as e:
            print(f"❌ [NETWORK ERROR] Failed to bind socket: {e}")
            return

        while True:
            try:
                client, _ = server.accept()
                data = client.recv(1024).decode('utf-8')
                if data:
                    # Parse the incoming JSON command
                    payload = json.loads(data)
                    self.command_queue.put(payload)
                client.close()
            except Exception:
                pass

    def evaluate(self, s, sy, p, snn, text="", haptic_level=0.0, **kwargs):
        """Checks the queue for new prompts and applies them to the system state."""
        
        # Process any new commands from the offsite network
        while not self.command_queue.empty():
            try:
                cmd = self.command_queue.get_nowait()
                self.active_phase_shift = float(cmd.get("phase_shift", self.active_phase_shift))
                self.active_bias_shift = float(cmd.get("bias_shift", self.active_bias_shift))
                print(f"   ⚡ [OFFSITE PROMPT APPLIED] Phase Shift: {self.active_phase_shift} | Bias Shift: {self.active_bias_shift}")
            except queue.Empty:
                break

        # Apply the remote overrides to the system's phase and synchronization
        adjusted_p = np.clip(p + self.active_phase_shift, -1.0, 1.0)
        adjusted_sy = np.clip(sy + self.active_bias_shift, 0.0, 1.0)
        
        # Calculate final resonance based on the overridden values
        final_signal = (s * 0.4) + (adjusted_sy * 0.3) + (abs(adjusted_p) * 0.3)
        return float(np.clip(final_signal, 0.0, 1.0))