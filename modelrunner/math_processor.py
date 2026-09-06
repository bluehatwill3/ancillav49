import json
import math
import re

class MathProcessor:
    def __init__(self, data_path):
        """Initializes the processor with the path to challenge_test.json."""
        with open(data_path, 'r') as f:
            self.dataset = json.load(f)
        
        # Define the operations registry
        self.ops = {
            'add': lambda x, y: x + y,
            'subtract': lambda x, y: x - y,
            'multiply': lambda x, y: x * y,
            'divide': lambda x, y: x / y,
            'sqrt': lambda x: math.sqrt(x),
            'power': lambda x, y: math.pow(x, y),
            'inverse': lambda x: 1 / x,
            'const_1': 1, 'const_2': 2, 'const_3': 3, 'const_4': 4, 
            'const_6': 6, 'const_10': 10, 'const_60': 60, 'const_100': 100
        }

    def evaluate_formula(self, formula):
        """Parses and evaluates the functional string formula."""
        # This is a simplified regex-based approach for demonstration.
        # For production-grade math parsing, look into libraries like 'sympy' or an AST parser.
        
        # Replace constants in string first
        for key in self.ops:
            if key.startswith('const_'):
                formula = formula.replace(key, str(self.ops[key]))
        
        # This simple eval is used here because the data format is structured as 
        # standard function calls, but please be careful with 'eval' in untrusted environments.
        # We will create a safe execution context by mapping functions.
        safe_dict = {
            'add': self.ops['add'],
            'subtract': self.ops['subtract'],
            'multiply': self.ops['multiply'],
            'divide': self.ops['divide'],
            'sqrt': self.ops['sqrt'],
            'power': self.ops['power'],
            'inverse': self.ops['inverse']
        }
        
        try:
            return eval(formula, {"__builtins__": None}, safe_dict)
        except Exception as e:
            return f"Error evaluating {formula}: {e}"

    def process_all(self):
        """Processes all items in the dataset."""
        results = []
        for entry in self.dataset:
            problem = entry.get('Problem')
            formula = entry.get('annotated_formula')
            value = self.evaluate_formula(formula)
            results.append({'problem': problem, 'result': value})
        return results

# Implementation Example:
# processor = MathProcessor('challenge_test.json')
# results = processor.process_all()
# for res in results:
#     print(f"Problem: {res['problem']} -> Result: {res['result']}")