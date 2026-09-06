import json
import re

class HolosynTokenizer:
    """
    Tokenizer for Holosyn v41. Supports math formulas and instruction tags.
    """
    def __init__(self):
        # Base tokens for communication tasks
        self.vocab = {
            "[PAD]": 0, "[UNK]": 1, "[BOS]": 2, 
            "[EOS]": 3, "[INSTRUCT]": 4
        }
        self.inv_vocab = {v: k for k, v in self.vocab.items()}

    def fit(self, dataset_path):
        """Builds vocabulary from the challenge_test.json file."""
        with open(dataset_path, 'r') as f:
            data = json.load(f)
            
        for entry in data:
            # Tokenize formula symbols and problem text
            formula = entry['annotated_formula']
            problem = entry['Problem']
            
            # Extract symbols (operators, parens, numbers)
            tokens = re.findall(r'[a-zA-Z_0-9.]+|\(|\)|,', formula)
            # Split problem into words
            words = problem.lower().split()
            
            for token in tokens + words:
                if token not in self.vocab:
                    idx = len(self.vocab)
                    self.vocab[token] = idx
                    self.inv_vocab[idx] = token

    def encode(self, text, is_instruction=False):
        """Converts string input to indices for the Spike Transformer."""
        tokens = ["[BOS]"]
        if is_instruction:
            tokens.append("[INSTRUCT]")
        
        # Simple whitespace splitting for now
        text_tokens = re.findall(r'[a-zA-Z_0-9.]+|\(|\)|,', text)
        tokens.extend(text_tokens)
        tokens.append("[EOS]")
        
        return [self.vocab.get(t, self.vocab["[UNK]"]) for t in tokens]

# Implementation Example:
# tokenizer = HolosynTokenizer()
# tokenizer.fit('challenge_test.json')
# encoded_input = tokenizer.encode("add(n0, const_10)", is_instruction=True)
# print(f"Encoded Indices: {encoded_input}")