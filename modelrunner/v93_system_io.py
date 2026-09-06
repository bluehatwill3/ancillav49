import sys
import os
import subprocess
import shlex
import numpy as np

# ──────────────────────────────────────────────────────────────────────
# 🔌 INTER-MODULE NAMESPACE BRIDGE
# ──────────────────────────────────────────────────────────────────────
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
# 🖥️ SYSTEM ROOT & I/O OBSERVER
# ──────────────────────────────────────────────────────────────────────
class SystemRootObserver(BaseObserver):
    """
    Holosyn V93: System Root & I/O Control Observer.
    Parses text telemetry for execution tags to control the mouse, 
    keyboard, and local file system via the command line.
    """
    def __init__(self, timeout_seconds=5.0):
        super().__init__()
        self.timeout = timeout_seconds
        print("   🖥️ [SYSTEM I/O] Hardware automation observer initialized.")

    def _execute_shell(self, command):
        """Safely executes a shell command and returns the exit code and output."""
        try:
            result = subprocess.run(
                command, 
                shell=True, 
                capture_output=True, 
                text=True, 
                timeout=self.timeout
            )
            if result.stdout:
                print(f"       [STDOUT]: {result.stdout.strip()[:150]}")
            if result.stderr:
                print(f"       [STDERR]: {result.stderr.strip()[:150]}")
            return result.returncode
        except subprocess.TimeoutExpired:
            print("   ❌ [OS TIMEOUT] Command exceeded execution limits.")
            return 1
        except Exception as e:
            print(f"   ❌ [OS FAULT] Execution failed: {e}")
            return 1

    def evaluate(self, s, sy, p, snn, text="", haptic_level=0.0, **kwargs):
        if not text:
            return 0.5

        clean_text = text.strip()
        exit_code = -1

        # 1. Standard Terminal Command Execution
        if clean_text.startswith("[CMD]"):
            cmd = clean_text.replace("[CMD]", "").strip()
            print(f"   ⚙️ [ROOT EXECUTION] Running: {cmd}")
            exit_code = self._execute_shell(cmd)

        # 2. Keyboard Typing Automation
        elif clean_text.startswith("[TYPE]"):
            type_text = clean_text.replace("[TYPE]", "").strip()
            # Escape single quotes to safely pass the string to xdotool
            safe_text = type_text.replace("'", "'\\''") 
            print(f"   ⌨️ [KEYBOARD MACRO] Typing: {type_text[:30]}...")
            exit_code = self._execute_shell(f"xdotool type '{safe_text}'")

        # 3. Mouse Movement Automation
        elif clean_text.startswith("[MOUSE]"):
            coords = clean_text.replace("[MOUSE]", "").strip()
            print(f"   🖱️ [MOUSE MACRO] Moving to: {coords}")
            exit_code = self._execute_shell(f"xdotool mousemove {coords}")

        # If no tags are found, return a neutral resonance
        if exit_code == -1:
            return np.clip((s + sy) / 2.0, 0.0, 1.0)

        # Map binary execution status to the continuous resonance matrix
        if exit_code == 0:
            # Command succeeded: Increase resonance harmony
            resonance = np.clip(0.75 + (s * 0.15) + (sy * 0.10), 0.0, 1.0)
        else:
            # Command failed: Drop resonance to indicate instability
            resonance = np.clip(0.25 - (abs(haptic_level) * 0.1), 0.0, 1.0)

        return float(resonance)