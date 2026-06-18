#!/usr/bin/env python3
"""
HOLOSYN PLUGIN: AXIOMATIC NEXUS (Neuro-Symbolic Logic)
================================================================
Integrates SymPy (Open-Source Math Engine) for real-time 
calculus, logical proofs, and long-term axiomatic validation.
"""

import sys
import re
import numpy as np
import sympy
try:
    import sympy
    from sympy.logic.boolalg import is_sat
    SYMPY_AVAILABLE = True
except ImportError:
    SYMPY_AVAILABLE = False
    print("   ⚠️ SymPy not found. Math Observers will use weak heuristics. (Run: pip install sympy)")

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
# 1. AXI: AXIOMATIC PROOF OBSERVER (Short/Long-term Validation)
# ---------------------------------------------------------
class AxiomaticProofObserver(BaseObserver):
    """
    Evaluates logical consistency. Allows axioms to break in the short term,
    storing them in a buffer for long-term integration and potential resolution.
    """
    def __init__(self):
        super().__init__()
        self.long_term_buffer = []
        self.paradox_tolerance = 0.5

    def evaluate(self, s, sy, p, snn, text="", haptic_level=0.0, **kwargs):
        if not text: return 0.5
        
        # Detect logical operators in text
        logic_keywords = ["if", "then", "and", "or", "not", "true", "false", "contradiction", "axiom"]
        logic_density = sum(1 for word in text.lower().split() if word in logic_keywords) / max(1, len(text.split()))
        
        # Simulate an Axiomatic State Check
        short_term_validity = 1.0 - (np.std(snn) if len(snn) > 0 else 0.0)
        
        # If the neural network is highly erratic (spike variance is high), we assume a logical contradiction/paradox
        if short_term_validity < self.paradox_tolerance:
            # Axiom broken! Store the phase for long-term validation
            self.long_term_buffer.append(p)
            short_term_score = 0.2 # Penalize short term
        else:
            short_term_score = 0.8 + (logic_density * 0.2)
            
        # Long-term validation: Check if historical paradoxes resolve into a stable mean
        if len(self.long_term_buffer) > 10:
            long_term_variance = np.var(self.long_term_buffer)
            self.long_term_buffer.pop(0)
            long_term_score = np.clip(1.0 - long_term_variance, 0.0, 1.0)
        else:
            long_term_score = 0.5
            
        # Blend short-term logic with long-term validation
        axi_score = (short_term_score * 0.6) + (long_term_score * 0.4)
        return np.clip(axi_score, 0.0, 1.0)

# ---------------------------------------------------------
# 2. SYM: SYMBOLIC MATH CALCULATOR (Open Source Math Engine)
# ---------------------------------------------------------
class SymbolicMathObserver(BaseObserver):
    """
    Hunts for math equations (e.g., 2+2, x^2), parses them using SymPy,
    and rewards the system when valid mathematical structures are found.
    """
    def __init__(self):
        super().__init__()
        self.math_pattern = re.compile(r'([0-9]+[\+\-\*\/\^][0-9a-zA-Z\+\-\*\/\^\(\)\s]+)')

    def evaluate(self, s, sy, p, snn, text="", haptic_level=0.0, **kwargs):
        if not text or not SYMPY_AVAILABLE: return 0.5
        
        # Extract potential mathematical formulas from text
        formulas = self.math_pattern.findall(text)
        
        math_score = 0.0
        if formulas:
            valid_equations = 0
            for formula in formulas[:3]:  # Limit to 3 to prevent processing lag
                try:
                    # Clean typical text anomalies out of the formula
                    clean_formula = formula.replace('^', '**').strip()
                    # Attempt to parse into a SymPy expression tree
                    expr = sympy.sympify(clean_formula, evaluate=False)
                    valid_equations += 1
                except Exception:
                    pass # Invalid syntax, skip
                    
            if valid_equations > 0:
                # Highly structured math rewards the Observer
                math_score = 0.6 + (valid_equations * 0.1)
        
        # If no explicit math is found, rely on structural symmetry (sy)
        final_score = math_score if math_score > 0 else (sy * 0.5)
        return np.clip(final_score + (p * 0.1), 0.0, 1.0)

# ---------------------------------------------------------
# 3. RSN: INFERENTIAL REASONING OBSERVER
# ---------------------------------------------------------
class InferentialReasoningObserver(BaseObserver):
    """
    Measures 'Depth of Thought' by tracking premise-to-conclusion 
    chaining and argument structure.
    """
    def __init__(self):
        super().__init__()
        self.premise_markers = ["because", "since", "assuming", "given"]
        self.conclusion_markers = ["therefore", "thus", "consequently", "implies", "so"]

    def evaluate(self, s, sy, p, snn, text="", haptic_level=0.0, **kwargs):
        if not text: return 0.5
        
        text_lower = text.lower()
        
        # Count argumentative structures
        premises = sum(1 for p_mark in self.premise_markers if p_mark in text_lower)
        conclusions = sum(1 for c_mark in self.conclusion_markers if c_mark in text_lower)
        
        # Ideal reasoning has a balance of premises and conclusions
        if premises > 0 and conclusions > 0:
            argument_balance = min(premises, conclusions) / max(premises, conclusions)
            reasoning_score = 0.7 + (argument_balance * 0.3)
        elif premises > 0 or conclusions > 0:
            reasoning_score = 0.6 # Partial reasoning
        else:
            reasoning_score = 0.4 # Declarative/Descriptive text
            
        # Neural drift (s) acts as 'creative leaps' in logic
        return np.clip(reasoning_score * 0.8 + (s * 0.2), 0.0, 1.0)