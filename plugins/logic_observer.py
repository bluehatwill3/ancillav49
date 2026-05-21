import re
import numpy as np
import __main__

# Dynamically links to your active Holosyn script's memory
BaseObserver = getattr(__main__, 'BaseObserver', object)

class CodeSyntaxObserver(BaseObserver):
    def evaluate(self, s, sy, p, snn, text="", haptic_level=0.0, **kwargs):
        if not text: return 0.5
        
        # Look for standard programming syntax operators and keywords
        code_markers = [r'def ', r'import ', r'\{', r'\}', r'=>', r'return ', r'class ', r'function', r'var ', r'let ']
        match_count = sum(1 for marker in code_markers if re.search(marker, text))
        
        # Calculate code density and force structural alignment
        density = np.clip(match_count / 3.0, 0.0, 1.0)
        return np.clip((density * 0.8) + (abs(p) * 0.2), 0.0, 1.0)