import re
import numpy as np
import __main__

BaseObserver = getattr(__main__, 'BaseObserver', object)

class CryptographicAnomalyObserver(BaseObserver):
    def evaluate(self, s, sy, p, snn, text="", haptic_level=0.0, **kwargs):
        if not text: return 0.5
        
        # Detect hexadecimal strings, base64 payloads, or long unbroken alphanumeric hashes
        hex_patterns = len(re.findall(r'\b[A-Fa-f0-9]{16,}\b', text))
        b64_patterns = len(re.findall(r'\b[A-Za-z0-9+/]{20,}={0,2}\b', text))
        wallet_patterns = len(re.findall(r'\b(1|3|bc1|0x)[a-zA-HJ-NP-Z0-9]{25,39}\b', text))
        
        anomaly_density = (hex_patterns + b64_patterns + wallet_patterns) * 0.6
        
        return np.clip(anomaly_density + (abs(p) * 0.1), 0.0, 1.0)