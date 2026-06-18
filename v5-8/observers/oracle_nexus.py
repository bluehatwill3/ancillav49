#!/usr/bin/env python3
"""
HOLOSYN PLUGIN: ORACLE NEXUS (Advanced Clairvoyance)
================================================================
Enhances the predictive layer of the Hive with Markov Chains,
Signal Autocorrelation (Deja Vu), and Chaos Theory (Lyapunov).
"""

import sys
import math
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
# 1. MKV: MARKOV PROPHECY OBSERVER (Probabilistic Clairvoyance)
# ---------------------------------------------------------
class MarkovProphecyObserver(BaseObserver):
    """
    Builds a real-time probability matrix of the system's phase shifts.
    It guesses the future based on statistical historical transitions.
    """
    def __init__(self):
        super().__init__()
        self.num_states = 10
        # Initialize a transition matrix with slight uniform probabilities
        self.transition_matrix = np.ones((self.num_states, self.num_states)) * 0.1
        self.last_state = 0

    def evaluate(self, s, sy, p, snn, text="", haptic_level=0.0, **kwargs):
        # 1. Quantize the continuous phase (p) into a discrete state bin (0 to 9)
        current_state = int(np.clip(p * self.num_states, 0, self.num_states - 1))
        
        # 2. What did the Markov Chain predict the current state would be?
        predicted_state_probs = self.transition_matrix[self.last_state]
        predicted_state = np.argmax(predicted_state_probs)
        
        # 3. Update the Transition Matrix based on what actually happened
        self.transition_matrix[self.last_state, current_state] += 1.0
        
        # Normalize the row so probabilities sum to 1.0
        row_sum = np.sum(self.transition_matrix[self.last_state])
        if row_sum > 0:
            self.transition_matrix[self.last_state] /= row_sum
            
        # 4. Score based on prediction accuracy
        if predicted_state == current_state:
            # Perfect prediction!
            mkv_score = 0.9 + (sy * 0.1)
        else:
            # Calculate how far off the prediction was
            error_distance = abs(predicted_state - current_state) / self.num_states
            mkv_score = np.clip(0.6 - error_distance, 0.0, 1.0)
            
        self.last_state = current_state
        return mkv_score

# ---------------------------------------------------------
# 2. DJV: DEJA VU OBSERVER (Temporal Autocorrelation)
# ---------------------------------------------------------
class DejaVuObserver(BaseObserver):
    """
    Searches for repeating geometric patterns in the timeline.
    If the current sequence of data mirrors a past sequence perfectly,
    it triggers a 'Deja Vu' resonance.
    """
    def __init__(self):
        super().__init__()
        self.history = []
        self.window_size = 50  # Keep track of the last 50 phase states

    def evaluate(self, s, sy, p, snn, text="", haptic_level=0.0, **kwargs):
        self.history.append(p)
        if len(self.history) > self.window_size:
            self.history.pop(0)
            
        # We need a decent history buffer to experience Deja Vu
        if len(self.history) == self.window_size:
            history_array = np.array(self.history)
            
            # Split history into 'deep past' and 'recent past'
            deep_past = history_array[:25]
            recent_past = history_array[25:]
            
            # Calculate Pearson correlation coefficient between the two timelines
            correlation_matrix = np.corrcoef(deep_past, recent_past)
            correlation = correlation_matrix[0, 1]
            
            # If correlation is NaN (e.g. flatline data), set to 0
            if np.isnan(correlation):
                correlation = 0.0
                
            # High positive correlation means the pattern is repeating exactly
            djv_score = np.clip((correlation * 0.6) + 0.4, 0.0, 1.0)
        else:
            djv_score = 0.5 # Neutral while building history
            
        return djv_score

# ---------------------------------------------------------
# 3. BTY: BUTTERFLY EFFECT OBSERVER (Chaos / Lyapunov)
# ---------------------------------------------------------
class ButterflyChaosObserver(BaseObserver):
    """
    Measures the 'Lyapunov Exponent'—how sensitive the future is to 
    tiny perturbations right now.
    """
    def __init__(self):
        super().__init__()
        self.last_p = 0.5
        self.last_snn_mean = 0.5

    def evaluate(self, s, sy, p, snn, text="", haptic_level=0.0, **kwargs):
        current_snn_mean = np.mean(snn) if len(snn) > 0 else 0.5
        
        # Delta X: How much did the input (neural spikes) change?
        delta_input = abs(current_snn_mean - self.last_snn_mean)
        
        # Delta Y: How much did the output phase (p) change as a result?
        delta_output = abs(p - self.last_p)
        
        # Ratio of Output Change to Input Change (Sensitivity)
        if delta_input > 0.001:
            sensitivity = delta_output / delta_input
        else:
            sensitivity = 0.0
            
        # The Lyapunov Exponent is roughly the log of this sensitivity
        # High positive value = Chaos. Negative/Zero = Stable/Predictable.
        lyapunov_proxy = math.log(sensitivity + 1e-5)
        
        # We want to measure the "Predictability" of the system.
        # If chaos is low, predictability is high.
        predictability = np.clip(1.0 - (abs(lyapunov_proxy) / 10.0), 0.0, 1.0)
        
        # Update states for next cycle
        self.last_p = p
        self.last_snn_mean = current_snn_mean
        
        # Blend predictability with the neural synchronization (sy)
        bty_score = (predictability * 0.7) + (sy * 0.3)
        return np.clip(bty_score, 0.0, 1.0)