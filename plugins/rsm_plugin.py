#!/usr/bin/env python3
"""
HOLOSYN PLUGIN: REDUNDANT SEMANTIC MANIFOLD (RSM) & GEODESIC (GEO)
================================================================
Based on Notebook trapap(7).ipynb

This plugin introduces PyTorch-based projection layers to evaluate 
text embeddings in a continuous phase space.
"""

import sys
import torch
import torch.nn as nn
import numpy as np
import math

# ---------------------------------------------------------
# DYNAMIC BASE CLASS RESOLUTION
# ---------------------------------------------------------
# We dynamically fetch BaseObserver from your main script's namespace 
# so the /plugin loader recognizes these classes correctly.
try:
    BaseObserver = sys.modules['__main__'].BaseObserver
except (KeyError, AttributeError):
    # Safe fallback just in case the plugin is run in isolation
    class BaseObserver:
        def evaluate(self, s, sy, p, snn, text="", haptic_level=0.0, **kwargs): 
            return 0.5

# ---------------------------------------------------------
# 1. RSM: REDUNDANT SEMANTIC MANIFOLD OBSERVER
# ---------------------------------------------------------
class RedundantSemanticObserver(BaseObserver):
    """
    Expands discrete tokens into a high-dimensional continuous space,
    evaluating the invariance loss of the textual manifold.
    """
    def __init__(self):
        super().__init__()
        # Mimicking the Projector class from trapap(7).ipynb
        self.vocab_size = 128
        self.embed_dim = 16
        self.phase_dim = 64
        
        # Project standard embeddings into a larger 'phase space'
        self.embedding = nn.Embedding(self.vocab_size, self.embed_dim)
        self.expansion = nn.Linear(self.embed_dim, self.phase_dim)
        self.activation = nn.Tanh()

    def evaluate(self, s, sy, p, snn, text="", haptic_level=0.0, **kwargs):
        if not text:
            return 0.5
            
        # Convert string to discrete ASCII tokens, clamped to vocab_size
        token_ids = [ord(c) % self.vocab_size for c in text[:64]]
        if not token_ids:
            return 0.5
            
        with torch.no_grad():
            x_tensor = torch.tensor(token_ids, dtype=torch.long)
            
            # Pass through Projector architecture
            embeds = self.embedding(x_tensor)
            phase_space = self.activation(self.expansion(embeds))
            
            # Calculate the invariance loss (mean absolute activation)
            invariance = torch.mean(torch.abs(phase_space)).item()
        
        # Combine the calculated manifold invariance with the system's current phase (p)
        rsm_score = np.clip(0.4 + (invariance * 0.4) + (s * 0.1) + (p * 0.1), 0.0, 1.0)
        return rsm_score

# ---------------------------------------------------------
# 2. GEO: GEODESIC PHASE OBSERVER
# ---------------------------------------------------------
class GeodesicPhaseObserver(BaseObserver):
    """
    Tracks the cosine similarity and geodesic distance (g_dist) of the 
    system's phase shifts across evaluation cycles.
    """
    def __init__(self):
        super().__init__()
        self.last_phase = 0.0

    def evaluate(self, s, sy, p, snn, text="", haptic_level=0.0, **kwargs):
        # Calculate cosine angle (Cos) between current phase and previous phase
        angle = p - self.last_phase
        cos_similarity = math.cos(angle)
        
        # Simulate geodesic distance (g_dist) using neural spike network (snn) density
        g_dist = np.std(snn) * 2.5 if len(snn) > 0 else 0.1
        
        # Update system history for the next cycle
        self.last_phase = p
        
        # Output favors high cosine alignment and stable geodesic traversal
        geo_score = np.clip(0.3 + (cos_similarity * 0.4) + (g_dist * 0.2) + (sy * 0.1), 0.0, 1.0)
        return geo_score