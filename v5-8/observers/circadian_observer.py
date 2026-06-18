import time
import math
import numpy as np
import __main__

BaseObserver = getattr(__main__, 'BaseObserver', object)

class CircadianRhythmObserver(BaseObserver):
    def evaluate(self, s, sy, p, snn, text="", haptic_level=0.0, **kwargs):
        # 24-hour cycle translated to seconds
        current_time = time.time()
        
        # Local hour approximation (0.0 to 24.0)
        hour_val = (current_time / 3600.0) % 24.0 
        
        # Sine wave peaking at noon (12:00) and bottoming out at midnight (0:00)
        wave = math.sin((hour_val - 6) * (math.pi / 12)) 
        
        # Combine the solar wave with the system's biological spiking network
        bio_sync = np.mean(snn) if len(snn) > 0 else 0.0
        
        return np.clip(0.5 + (wave * 0.3) + (bio_sync * 0.2), 0.0, 1.0)