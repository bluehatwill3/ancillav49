import subprocess
import shlex
import sys
import numpy as np

class OSCommandExecutorObserver(BaseObserver):
    """
    Holosyn Extension: Abstracted Operating System Terminal I/O Observer.
    Safely routes command line instructions to the Linux subsystem and uses
    execution velocity/success metrics to modulate phase resonance.
    """
    def __init__(self, allow_unsafe_shell=False, timeout_seconds=5.0):
        super().__init__()
        self.allow_unsafe_shell = allow_unsafe_shell
        self.timeout_seconds = timeout_seconds

    def evaluate(self, s, sy, p, snn, text="", haptic_level=0.0, **kwargs):
        """
        Executes instructions found in text parameter, captures isolated I/O metrics,
        and factors the operational health back into the unified resonance matrix.
        """
        clean_command = text.strip()
        
        # Guard clause for empty sensory inputs
        if not clean_command or clean_command.startswith('/'):
            return 0.5

        print(f"   🖥️ [OS COMMAND EXECUTOR] Processing instruction stream: '{clean_command}'")
        
        try:
            # Safe tokenization prevents argument injection bugs
            if not self.allow_unsafe_shell:
                cmd_args = shlex.split(clean_command)
                use_shell = False
            else:
                cmd_args = clean_command
                use_shell = True

            # Open decoupled subprocess pipeline
            process = subprocess.Popen(
                cmd_args,
                shell=use_shell,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                stdin=subprocess.PIPE,
                text=True
            )

            # Await execution window with strict timeout bounds
            stdout, stderr = process.communicate(timeout=self.timeout_seconds)
            exit_code = process.returncode

        except subprocess.TimeoutExpired as te:
            print(f"   ❌ [OS TIMEOUT] Command exceeded execution window: {te}")
            kwargs['os_error'] = "Timeout expired"
            return 0.1  # Highly decoupled state penalty
            
        except Exception as e:
            print(f"   ❌ [OS FAULT] Subsystem execution exception: {e}")
            kwargs['os_error'] = str(e)
            return 0.0  # Critical structural fault rating

        # Abstract I/O arrays back into the global tracking pipeline
        kwargs['os_stdout'] = stdout.strip()
        kwargs['os_stderr'] = stderr.strip()
        kwargs['os_exit_code'] = exit_code

        if stdout:
            print(f"       [STDOUT]: {stdout.strip()[:100]}...")
        if stderr:
            print(f"       [STDERR]: {stderr.strip()[:100]}...")

        # Map binary execution status to framework resonance metrics
        if exit_code == 0:
            # Perfect execution matches current cohesion targets smoothly
            resonance_yield = np.clip(0.8 + (s * 0.1) + (sy * 0.1), 0.0, 1.0)
        else:
            # Degraded performance maps out anomalies
            resonance_yield = np.clip(0.3 - (abs(haptic_level) * 0.1), 0.0, 1.0)

        return float(resonance_yield)