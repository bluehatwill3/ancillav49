#!/usr/bin/env python3
"""
HOLOSYN V41: MASTER ALGEBRAIC COMPLEX & SYMBOLIC MATRIX OBSERVER
====================================================================
Hardware Target: 16GB RAM | i5 8-Core (CPU-Only Performance Optimized)
Role: Safe parsing and evaluation of symbolic math formulas to map phase resonance.
"""

import sys
import os
import ast
import operator
import math
import numpy as np

# ──────────────────────────────────────────────────────────────────────
# 🔌 INTER-MODULE NAMESPACE BRIDGE
# ──────────────────────────────────────────────────────────────────────
BaseObserver = None
avenues = ['__main__', 'nexus', 'core', 'observer', 'main', 'harvest_manager']
for module_name in avenues:
    if module_name in sys.modules:
        mod = sys.modules[module_name]
        if hasattr(mod, 'BaseObserver'):
            BaseObserver = getattr(mod, 'BaseObserver')
            break

if BaseObserver is None:
    class BaseObserver:
        def evaluate(self, s, sy, p, snn, text="", haptic_level=0.0, **kwargs): 
            return 0.5

# ──────────────────────────────────────────────────────────────────────
# 🧮 ALGEBRAIC COGNITIVE OBSERVER
# ──────────────────────────────────────────────────────────────────────
class AlgebraCognitiveObserver(BaseObserver):
    """
    Parses annotated mathematical formulas safely from incoming sensory text log
    streams and converts numerical output variance into system phase resonance points.
    """
    def __init__(self):
        super().__init__()
        
        # Safe math operator mappings avoiding raw eval string executions
        self.operators = {
            'add': operator.add,
            'subtract': operator.sub,
            'multiply': operator.mul,
            'divide': lambda a, b: operator.truediv(a, b) if b != 0 else 1.0,
            'power': operator.pow,
            'sqrt': math.sqrt
        }
        
        # Constant vocabulary mapping matching your constant list specifications
        self.constants = {
            'const_1': 1.0,
            'const_2': 2.0,
            'const_3': 3.0,
            'const_4': 4.0,
            'const_6': 6.0,
            'const_10': 10.0,
            'const_60': 60.0,
            'const_100': 100.0,
            'const_1000': 1000.0
        }

    def _safe_eval(self, node):
        """Recursively parses an Abstract Syntax Tree node for math operations."""
        if isinstance(node, ast.Num):  # Raw numeric literals
            return float(node.n)
            
        elif isinstance(node, ast.Name):  # Constant identifiers
            name = node.id
            if name in self.constants:
                return self.constants[name]
            return 1.0  # Fallback token for unrecognized variables
            
        elif isinstance(node, ast.Call):  # Function calls like add() or multiply()
            func_name = node.func.id
            if func_name in self.operators:
                args = [self._safe_eval(arg) for arg in node.args]
                if func_name == 'sqrt' and len(args) == 1:
                    return self.operators[func_name](max(0.0, args[0]))
                elif len(args) == 2:
                    return self.operators[func_name](args[0], args[1])
            return 0.5
            
        elif isinstance(node, ast.Expression):
            return self._safe_eval(node.body)
            
        return 0.0

    def parse_formula_string(self, formula_text: str) -> float:
        """Cleans, normalizes, and evaluates a formula token safely."""
        try:
            # Normalize brackets and structural expressions
            clean_str = formula_text.strip().replace("const_pi", str(math.pi))
            tree = ast.parse(clean_str, mode='eval')
            return float(self._safe_eval(tree))
        except Exception:
            return 0.5

    def evaluate(self, s, sy, p, snn, text="", haptic_level=0.0, **kwargs):
        """
        Intercepts text payloads containing analytical formulas, evaluates them, 
        and maps numerical consistency back into system governance space.
        """
        if not text or ("add" not in text and "divide" not in text and "multiply" not in text):
            # No explicit mathematical formula detected, pass neutral response
            return np.clip((s + sy) / 2.0, 0.0, 1.0)

        print(f"   🧮 [ALGEBRA OBSERVER] Parsing formula stream: '{text[:80]}...'")
        
        # Process calculation output
        math_result = self.parse_formula_string(text)
        kwargs['algebra_output'] = math_result
        
        # Calculate a variance baseline to protect stability
        # If the output is an exceptionally massive infinity float, stabilize it safely
        if math.isnan(math_result) or math.isinf(math_result):
            math_result = 1.0
            
        # Standardize resonance scaling map (Sigmoidal mapping proxy for boundary containment)
        normalized_math = math.tanh(math_result / 1000.0) if math_result > 0 else 0.5
        
        final_resonance = np.clip(
            (s * 0.3) + 
            (normalized_math * 0.4) + 
            ((1.0 - abs(p)) * 0.3), 
            0.0, 1.0
        )
        
        print(f"       [EVALUATION VALUE]: {math_result:.4f} | [MAPPED RESONANCE]: {final_resonance:.4f}")
        return float(final_resonance)