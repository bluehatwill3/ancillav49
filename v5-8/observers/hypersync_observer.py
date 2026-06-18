import numpy as np
import __main__

BaseObserver = getattr(__main__, 'BaseObserver', object)

class HyperSynchronyObserver(BaseObserver):
    def evaluate(self, s, sy, p, snn, text="", haptic_level=0.0, **kwargs):
        # Measure the absolute distance between semantic coherence and structural synchrony
        divergence = abs(s - sy)
        
        # High reward (close to 1.0) when divergence is near 0.0
        synchrony = 1.0 - divergence
        
        # Boost based on haptic physical rumble
        return np.clip(synchrony * 0.8 + haptic_level * 0.2, 0.0, 1.0)