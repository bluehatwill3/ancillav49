import os
import random
import torch
import numpy as np

try:
    from __main__ import BaseObserver, TransformerCore
except ImportError:
    class BaseObserver:
        def evaluate(self, s, sy, p, snn, text="", haptic_level=0.0, **kwargs): return 0.5
    class TransformerCore:
        pass # Fallback if loaded outside Holosyn

class ManifoldLegionObserver(BaseObserver):
    """
    Manages THOUSANDS of .pt files via Stochastic MoE (Mixture of Experts).
    Prevents OOM crashes by only waking up a small committee of models per tick.
    """
    def __init__(self, vault_dir="./vaults"):
        super().__init__()
        self.vault_dir = vault_dir
        self.manifold_registry = []
        self.committee_size = 5 # How many models to wake up per tick
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        
        self._map_legion()

    def _map_legion(self):
        """Indexes all .pt files without loading them into memory."""
        print("🔍 [LEGION] Mapping Manifold Vaults...")
        for root, _, files in os.walk(self.vault_dir):
            for file in files:
                if file.endswith(('.pt', '.pth')):
                    self.manifold_registry.append(os.path.join(root, file))
        print(f"   ✅ [LEGION] Discovered {len(self.manifold_registry)} dormant manifolds.")

    def evaluate(self, s, sy, p, snn, text="", haptic_level=0.0, **kwargs):
        if not self.manifold_registry:
            return 0.5

        # 1. Draft the Committee (Random Stochastic Selection)
        committee_paths = random.sample(
            self.manifold_registry, 
            min(self.committee_size, len(self.manifold_registry))
        )
        
        # 2. Extract latent input from kwargs or generate fallback
        latent_input = kwargs.get('modality_embedding', torch.tensor([[[0.5, sy, p, np.mean(snn), s]]], dtype=torch.float32))

        committee_votes = []
        
        # 3. Wake, Evaluate, and Terminate (Memory Safe)
        for path in committee_paths:
            try:
                # Instantiate a blank core
                temp_core = TransformerCore().to(self.device)
                # Load weights strictly for this tick
                temp_core.assimilate(torch.load(path, map_location=self.device, weights_only=True))
                temp_core.eval()
                
                with torch.no_grad():
                    vote = temp_core(latent_input.to(self.device)).mean().item()
                    committee_votes.append(vote)
                    
            except Exception as e:
                pass # Fail silently if a specific .pt file is corrupted
                
            finally:
                # Destroy the object to free VRAM immediately
                del temp_core 

        # Return the aggregated consensus of the active committee
        if committee_votes:
            return float(np.clip(np.mean(committee_votes), 0.0, 1.0))
        return 0.5