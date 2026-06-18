import numpy as np
import __main__

BaseObserver = getattr(__main__, 'BaseObserver', object)

class FractalChaosObserver(BaseObserver):
    def evaluate(self, s, sy, p, snn, text="", haptic_level=0.0, **kwargs):
        # Normalize phase to a growth rate (r) between 2.5 and 4.0 (The Chaos Threshold)
        r = 2.5 + (abs(p) % 1.0) * 1.5
        
        # Iterate the logistic map: x_next = r * x * (1 - x)
        x = 0.5 
        for _ in range(5): 
            x = r * x * (1 - x)
            
        return np.clip(x, 0.0, 1.0)