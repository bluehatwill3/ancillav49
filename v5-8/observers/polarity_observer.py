import numpy as np
import __main__

BaseObserver = getattr(__main__, 'BaseObserver', object)

class PolarityExtremismObserver(BaseObserver):
    def evaluate(self, s, sy, p, snn, text="", haptic_level=0.0, **kwargs):
        extreme_words = ["always", "never", "hate", "destroy", "best", "worst", "impossible", "absolute", "everything", "nothing"]
        word_count = len(text.split())
        if word_count == 0: return 0.5
        
        extremity_hits = sum(1 for w in extreme_words if w in text.lower())
        polarization_score = np.clip((extremity_hits * 2.0) / max(1, word_count / 10), 0.0, 1.0)
        
        # Spike the score if the biological SNN voltage is also erratic
        snn_var = np.std(snn) if len(snn) > 0 else 0.0
        return np.clip(polarization_score * 0.7 + snn_var * 0.3, 0.0, 1.0)