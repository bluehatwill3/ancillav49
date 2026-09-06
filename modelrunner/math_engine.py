import math
import re
import json

class MathEngine:
    """
    Parses and executes mathematical formulas from the dataset.
    Handles nested structures like add(divide(n0, const_10), ...)
    """
    def __init__(self):
        # Mapping string operations to Python functions
        self.ops = {
            'add': lambda x, y: x + y,
            'subtract': lambda x, y: x - y,
            'multiply': lambda x, y: x * y,
            'divide': lambda x, y: x / y,
            'sqrt': lambda x: math.sqrt(x),
            'power': lambda x, y: math.pow(x, y),
            'inverse': lambda x: 1 / x,
            'factorial': lambda x: math.factorial(int(x))
        }
        
        # Mapping constants defined in your context
        self.constants = {
            'const_1': 1, 'const_2': 2, 'const_3': 3, 'const_4': 4,
            'const_6': 6, 'const_10': 10, 'const_60': 60, 'const_100': 100
        }

    def tokenize(self, formula):
        """Splits the formula string into meaningful components."""
        # Regex finds words, numbers, and parentheses
        return re.findall(r'[a-zA-Z_0-9.]+|\(|\)|,', formula)

    def parse_expression(self, tokens):
        """Recursively parses tokens into nested values."""
        token = tokens.pop(0)

        if token in self.ops:
            # It's a function: parse its arguments
            args = []
            tokens.pop(0) # Remove opening '('
            while tokens[0] != ')':
                args.append(self.parse_expression(tokens))
                if tokens[0] == ',':
                    tokens.pop(0) # Remove comma
            tokens.pop(0) # Remove closing ')'
            return self.ops[token](*args)
        
        elif token in self.constants:
            return self.constants[token]
        
        elif token.startswith('n'): # Handles variables like n0, n1
            return 0 # Placeholder: replace with actual dataset variable logic
        
        else:
            # It's a raw number
            return float(token)

    def process(self, formula_string):
        """Main entry point to evaluate a formula."""
        tokens = self.tokenize(formula_string)
        return self.parse_expression(tokens)

# Example Usage
if __name__ == "__main__":
    engine = MathEngine()
    
    # Test formula from dataset
    # "add(divide(1000, const_10), ...)"
    formula = "add(divide(1000, const_10), const_2)"
    result = engine.process(formula)
    print(f"Formula: {formula} -> Result: {result}")