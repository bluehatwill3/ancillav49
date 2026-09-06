#!/usr/bin/env python3
"""
HOLOSYN LOGIC NEXUS (V41)
=========================
A unified mathematical core for Boolean, Combinatorial, and 
Probabilistic reasoning. Designed for low-latency, plug-and-play 
integration into the Holosyn framework.
"""

import math
import numpy as np
from itertools import permutations, combinations

# Namespace bridge for BaseObserver
try:
    from __main__ import BaseObserver
except ImportError:
    class BaseObserver:
        def evaluate(self, s, sy, p, snn, text="", haptic_level=0.0, **kwargs): return 0.5

class HolosynLogicNexus(BaseObserver):
    def __init__(self):
        super().__init__()
        self.registry = {}
        
    # --- COMBINATORIAL ENGINE ---
    def compute_nPr(self, n, r): return math.perm(n, r)
    def compute_nCr(self, n, r): return math.comb(n, r)

    # --- BOOLEAN LOGIC ENGINE ---
    def apply_logic(self, gate: str, vals: List[bool]) -> bool:
        if gate == "AND": return all(vals)
        if gate == "OR": return any(vals)
        if gate == "NOT": return not vals[0]
        if gate == "XOR": return sum(vals) % 2 != 0
        return False

    # --- VARIABLE INDEPENDENCE ---
    def check_independence(self, p_a: float, p_b: float, p_joint: float) -> bool:
        """Independence test: P(A ∩ B) == P(A) * P(B)"""
        return np.isclose(p_joint, (p_a * p_b))

    def evaluate(self, s, sy, p, snn, text="", haptic_level=0.0, **kwargs):
        """
        Processes text for logical keys.
        Example text: "COMBINE 10 3" or "AND TRUE FALSE"
        """
        # Parsing Layer
        tokens = text.lower().split()
        if not tokens: return 0.5
        
        # Branch 1: Combinatorics
        if "permute" in tokens[0]:
            n, r = int(tokens[1]), int(tokens[2])
            val = self.compute_nPr(n, r)
            return np.clip(val / 1000.0, 0.0, 1.0)
            
        # Branch 2: Boolean
        elif tokens[0] in ["and", "or", "xor"]:
            vals = [t == "true" for t in tokens[1:]]
            res = self.apply_logic(tokens[0].upper(), vals)
            return 1.0 if res else 0.0
            
        # Branch 3: Independence Logic (P_A, P_B, Joint)
        elif "independent" in tokens[0]:
            pa, pb, pj = float(tokens[1]), float(tokens[2]), float(tokens[3])
            return 1.0 if self.check_independence(pa, pb, pj) else 0.0
            
        return 0.5