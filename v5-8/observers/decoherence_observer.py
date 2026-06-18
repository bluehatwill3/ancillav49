import numpy as np
import __main__

BaseObserver = getattr(__main__, 'BaseObserver', object)

class QuantumDecoherenceObserver(BaseObserver):
    def __init__(self):
        self.phase_history = []
        
    def evaluate(self, s, sy, p, snn, text="", haptic_level=0.0, **kwargs):
        self.phase_history.append(p)
        if len(self.phase_history) > 20: 
            self.phase_history.pop(0)
            
        if len(self.phase_history) < 10: 
            return 0.5
            
        # If phase is TOO stable, the system has stagnated. We force decoherence.
        variance = np.var(self.phase_history)
        
        if variance < 0.005:
            decoherence_penalty = 0.85  # Spike the entropy!
        else:
            decoherence_penalty = 0.0
            
        return np.clip(1.0 - decoherence_penalty - abs(sy * 0.1), 0.0, 1.0)