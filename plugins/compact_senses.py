#!/usr/bin/env python3
"""
HOLOSYN PLUGIN: COMPACT AUDIO & HAPTIC SENSES
================================================================
A zero-dependency, ultra-lightweight plugin that simulates 
acoustic resonance and haptic physics without heavy ML models.
"""

import sys
import math
import re
import numpy as np

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
# 1. ACO: ACOUSTIC PHONETIC OBSERVER (Compact Audio)
# ---------------------------------------------------------
class AcousticPhoneticObserver(BaseObserver):
    """
    Analyzes the 'sound' of the text using rhythmic and phonetic heuristics
    rather than heavy audio-processing neural networks.
    """
    def __init__(self):
        super().__init__()
        self.vowels = set("aeiouyAEIOUY")
        
    def evaluate(self, s, sy, p, snn, text="", haptic_level=0.0, **kwargs):
        if not text:
            return 0.5
            
        # 1. Calculate Resonance (Vowel to Consonant Ratio)
        # Vowels carry acoustic energy; consonants act as transients/clicks.
        v_count = sum(1 for char in text if char in self.vowels)
        c_count = sum(1 for char in text if char.isalpha() and char not in self.vowels)
        
        total_chars = max(1, v_count + c_count)
        vowel_density = v_count / total_chars
        
        # 2. Calculate Rhythm (Word length variance)
        words = text.split()
        if len(words) > 1:
            word_lengths = [len(w) for w in words]
            rhythm_variance = np.var(word_lengths)
            # Normalize variance to a 0-1 scale
            rhythm_score = np.clip(rhythm_variance / 10.0, 0.0, 1.0)
        else:
            rhythm_score = 0.5
            
        # Combine into an Acoustic Energy Score
        # High score = Highly resonant, rhythmic text
        aco_score = (vowel_density * 0.6) + (rhythm_score * 0.4)
        
        # Blend with system phase
        return np.clip(aco_score * 0.8 + (p * 0.2), 0.0, 1.0)

# ---------------------------------------------------------
# 2. KHP: KINEMATIC HAPTIC OBSERVER (Simulated Physics)
# ---------------------------------------------------------
class KinematicHapticObserver(BaseObserver):
    """
    Simulates a 1D Mass-Spring-Damper system. The text and neural spikes
    apply physical 'force' to a virtual spring, generating haptic feedback.
    """
    def __init__(self):
        super().__init__()
        # Physics Parameters
        self.velocity = 0.0
        self.position = 0.0
        self.spring_constant = 0.15  # Stiffness
        self.damping = 0.85          # Friction (1.0 = no friction)

    def evaluate(self, s, sy, p, snn, text="", haptic_level=0.0, **kwargs):
        # 1. Calculate Incoming Force 
        # Force is driven by neural spikes and the system's inherent haptic feedback
        spike_force = np.mean(snn) if len(snn) > 0 else 0.0
        external_force = (haptic_level * 1.5) + (spike_force * 0.5)
        
        # 2. Apply Hooke's Law (F = -kx) and Damping
        acceleration = external_force - (self.spring_constant * self.position)
        self.velocity = (self.velocity + acceleration) * self.damping
        self.position += self.velocity
        
        # 3. Calculate Tactile "Rumble"
        # Rumble is the absolute kinetic energy of our virtual spring
        kinetic_energy = 0.5 * (self.velocity ** 2)
        
        # Output limits to a 0.0 - 1.0 scale
        khp_score = np.clip(kinetic_energy * 5.0, 0.0, 1.0)
        
        return khp_score

# ---------------------------------------------------------
# 3. SXM: SYNESTHETIC CROSS-MODAL OBSERVER
# ---------------------------------------------------------
class SynestheticObserver(BaseObserver):
    """
    Monitors the interference pattern between simulated Audio (pacing) 
    and simulated Haptics (vibration voltage).
    """
    def __init__(self):
        super().__init__()
        self.history = []

    def evaluate(self, s, sy, p, snn, text="", haptic_level=0.0, **kwargs):
        # Determine punctuation density (acts as audio 'beats')
        punctuation = sum(1 for char in text if char in ".,!?-_:;")
        beat_density = punctuation / max(1, len(text))
        
        # Cross-multiply audio beats with physical haptic voltage
        synesthetic_blend = beat_density * haptic_level * 10.0
        
        # Track historical variance (synesthesia thrives on changing patterns)
        self.history.append(synesthetic_blend)
        if len(self.history) > 10:
            self.history.pop(0)
            
        pattern_variance = np.var(self.history) if len(self.history) > 1 else 0.0
        
        sxm_score = np.clip(0.4 + (synesthetic_blend * 0.3) + (pattern_variance * 2.0), 0.0, 1.0)
        return sxm_score