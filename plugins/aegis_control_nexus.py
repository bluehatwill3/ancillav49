#!/usr/bin/env python3
"""
HOLOSYN PLUGIN: AEGIS CONTROL DECK 
================================================================
A Meta-Control layer to harness, throttle, and validate the 
Ethereal, Oracle, and Chaos observers.
"""

import sys
import math
import numpy as np
from collections import deque

# ---------------------------------------------------------
# DYNAMIC BASE CLASS RESOLUTION
# ---------------------------------------------------------
try:
    BaseObserver = sys.modules['__main__'].BaseObserver
except (KeyError, AttributeError):
    class BaseObserver:
        def evaluate(self, s, sy, p, snn, text="", haptic_level=0.0, **kwargs): 
            return 0.5

# ---------------------------------------------------------
# 1. CVD: CLAIRVOYANT VALIDATOR (The Oracle Judge)
# ---------------------------------------------------------
class ClairvoyantValidatorObserver(BaseObserver):
    """
    Monitors the stability of the timeline. If the phase (p) shifts too 
    violently (usually caused by Oracle/Chaos modes hallucinating), 
    this observer spikes to force a 'Grounding' reset.
    """
    def __init__(self):
        super().__init__()
        self.phase_history = deque(maxlen=15)
        self.volatility_threshold = 0.35

    def evaluate(self, s, sy, p, snn, text="", haptic_level=0.0, **kwargs):
        self.phase_history.append(p)
        
        if len(self.phase_history) < 5:
            return 0.5 # Not enough data to judge yet
            
        # Calculate the volatility (standard deviation) of recent predictions/phases
        volatility = np.std(self.phase_history)
        
        # If volatility exceeds our safety threshold, the system is hallucinating
        if volatility > self.volatility_threshold:
            # Output a massive score to OVERRIDE the Oracle models
            validation_score = 0.95
        else:
            # System is stable, let the Oracles do their thing
            validation_score = 0.1 + (volatility * 0.5)
            
        return np.clip(validation_score, 0.0, 1.0)

# ---------------------------------------------------------
# 2. TTH: AEGIS TETHER (Anti-Chaos Anchor)
# ---------------------------------------------------------
class AegisTetherObserver(BaseObserver):
    """
    Acts as an elastic bungee cord. Monitors the divergence between 
    Neural Drift (s) and Structural Sync (sy). Prevents Astral Projection 
    from permanently snapping the network.
    """
    def __init__(self):
        super().__init__()
        self.tension = 0.0

    def evaluate(self, s, sy, p, snn, text="", haptic_level=0.0, **kwargs):
        # Calculate divergence between logic/structure (sy) and abstract drift (s)
        divergence = abs(s - sy)
        
        # If divergence is high, tension on the tether increases
        self.tension = (self.tension * 0.8) + (divergence * 0.2)
        
        # If neural spikes are flatlining (Void state) or exploding (Chaos state)
        snn_mean = np.mean(snn) if len(snn) > 0 else 0.5
        snn_extremity = abs(snn_mean - 0.5) * 2.0
        
        # The Tether scores highest when the system is dangerously close to the edge
        tether_score = (self.tension * 0.6) + (snn_extremity * 0.4)
        
        # If the tether score gets too high, it becomes the Governor and stabilizes the hive
        return np.clip(tether_score, 0.0, 1.0)

# ---------------------------------------------------------
# 3. FCS: FOCUS GATE (Signal vs. Noise Filter)
# ---------------------------------------------------------
class MetacognitiveFocusObserver(BaseObserver):
    """
    Calculates the Shannon Entropy of the input stream. 
    If you feed it highly logical data (code, math), it locks the system 
    into a high-focus state, effectively muting the Ethereal observers.
    """
    def __init__(self):
        super().__init__()

    def evaluate(self, s, sy, p, snn, text="", haptic_level=0.0, **kwargs):
        if not text: return 0.5
        
        # Calculate Shannon Entropy (Information Density)
        # High entropy = random noise/gibberish. Low entropy = highly structured logic.
        char_counts = {}
        for char in text:
            char_counts[char] = char_counts.get(char, 0) + 1
            
        total_chars = len(text)
        entropy = 0.0
        for count in char_counts.values():
            prob = count / total_chars
            entropy -= prob * math.log2(prob)
            
        # Normalize entropy (typical English text is around 4.0 to 5.0)
        # Code/Math is usually lower (more repeating symbols). Pure noise is high.
        normalized_entropy = np.clip(entropy / 8.0, 0.0, 1.0)
        
        # Focus is the INVERSE of entropy. 
        # Highly structured text = High Focus.
        focus = 1.0 - normalized_entropy
        
        # If the haptic level is buzzing too hard, it distracts focus
        distraction = np.clip(haptic_level * 0.5, 0.0, 1.0)
        
        fcs_score = np.clip(focus - distraction + (sy * 0.2), 0.0, 1.0)
        return fcs_score