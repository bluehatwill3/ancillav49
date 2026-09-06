import json
import torch
from math_engine import MathEngine  # Your parser logic
from tokenizer import HolosynTokenizer
from training_loop import TrainingLoop
from spike_transformer import SpikeTransformer

def run_pipeline():
    # 1. Setup Configuration
    # We reference the paths provided in your Holosyn archive[cite: 14, 15]
    DATASET_PATH = 'challenge_test.json'
    
    print("Initializing Holosyn Pipeline...")
    
    # 2. Tokenize the Dataset
    tokenizer = HolosynTokenizer()
    tokenizer.fit(DATASET_PATH)
    
    # 3. Model Initialization
    # Assuming vocab size from tokenizer and d_model configuration
    model = SpikeTransformer(vocab_size=len(tokenizer.vocab), d_model=64)
    
    # 4. Load Data and Train
    with open(DATASET_PATH, 'r') as f:
        dataset = json.load(f)
        
    print(f"Loaded {len(dataset)} math problems for training.")
    
    # Initialize and execute the loop
    trainer = TrainingLoop(model, dataset)
    trainer.run(epochs=5)
    
    print("Training complete. System ready for inference.")

if __name__ == "__main__":
    run_pipeline()