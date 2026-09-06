import torch
import torch.nn as nn
import torch.optim as optim
import json
import os
from math_engine import MathEngine  # Your parser
from tokenizer import HolosynTokenizer
from spike_transformer import SpikeTransformer

class HolosynOrchestrator:
    def __init__(self, data_path, config_path="config.json"):
        self.data_path = data_path
        self.config_path = config_path
        self.tokenizer = HolosynTokenizer()
        self.tokenizer.fit(data_path)
        self.model = SpikeTransformer(vocab_size=len(self.tokenizer.vocab), d_model=64)
        self.optimizer = optim.Adam(self.model.parameters(), lr=0.001)
        self.criterion = nn.MSELoss()

    def update_system(self, key, value):
        """System Modification API to update configuration."""
        config = {}
        if os.path.exists(self.config_path):
            with open(self.config_path, 'r') as f:
                config = json.load(f)
        config[key] = value
        with open(self.config_path, 'w') as f:
            json.dump(config, f, indent=4)
        print(f"[System] Updated {key} to {value}")

    def train_step(self, entry):
        """Single training iteration with Backpropagation."""
        formula = entry['annotated_formula']
        encoded = self.tokenizer.encode(formula)
        
        # Prepare Tensors
        input_tensor = torch.tensor(encoded, dtype=torch.long).unsqueeze(0)
        target = torch.randn(1, 64) # Placeholder for your target latent representation

        # Backpropagation
        self.optimizer.zero_grad()
        output = self.model(input_tensor)
        
        # Squeeze output to match target shape
        loss = self.criterion(output.mean(dim=1), target)
        loss.backward() # Backpropagation
        self.optimizer.step()
        
        return loss.item()

    def run(self, epochs=5):
        with open(self.data_path, 'r') as f:
            dataset = json.load(f)
            
        for epoch in range(epochs):
            epoch_loss = 0
            for entry in dataset:
                epoch_loss += self.train_step(entry)
            
            avg_loss = epoch_loss / len(dataset)
            print(f"Epoch {epoch+1} - Loss: {avg_loss:.4f}")
            self.update_system(f"epoch_{epoch+1}_loss", avg_loss)

if __name__ == "__main__":
    # Pointing to the archive data path
    orchestrator = HolosynOrchestrator('challenge_test.json')
    orchestrator.run()