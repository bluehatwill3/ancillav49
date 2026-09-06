"""
===============================================================================
SECTION 1: OUTDOOR TELEMETRY LEXICON & MULTISPECTRAL PERCEPTION ENGINE
===============================================================================
"""

import math
import random
from typing import Dict, List, Tuple
import cv2
import numpy as np
import torch
import torch.nn as nn

# -----------------------------------------------------------------------------
# 1. OUTDOOR SYSTEM CONFIGURATION
# -----------------------------------------------------------------------------
class OutdoorConfig:
    vocab_size: int = 6000
    max_seq_len: int = 96
    embed_dim: int = 128
    num_heads: int = 4
    num_layers: int = 2
    
    # 6 Macro Field Actions:
    # 0: LOG_FIELD_METRICS
    # 1: VARIABLE_RATE_FERTIGATION (Side-dress NPK)
    # 2: CENTER_PIVOT_IRRIGATION (Water mm)
    # 3: DISPATCH_SCOUTING_DRONE (High-res weed inspection)
    # 4: DEPLOY_ANTI_FROST_WIND_MACHINES
    # 5: DELAY_SPRAYING_HOLD (Adverse weather hold)
    num_actions: int = 6
    
    spike_threshold: float = 0.85
    leak_rate: float = 0.15
    batch_size: int = 32
    epochs: int = 8
    lr: float = 1e-3
    device: str = "cuda" if torch.cuda.is_available() else "cpu"
    save_path: str = "outdoor_field_brain.pt"

CONFIG = OutdoorConfig()


# -----------------------------------------------------------------------------
# 2. MULTISPECTRAL PERCEPTION FRONTEND (Aerial / Drone Imagery)
# -----------------------------------------------------------------------------
class OutdoorVisionFrontend:
    """
    Processes simulated Red and Near-Infrared (NIR) bands to extract:
    - NDVI (Normalized Difference Vegetation Index): (NIR - RED) / (NIR + RED)
    - Weed Density: Localized anomalies of high vigor outside standard rows
    - Canopy Ground Cover Ratio
    """
    @staticmethod
    def process_multispectral_bands(red_band: np.ndarray, nir_band: np.ndarray) -> Dict[str, float]:
        red_f = red_band.astype(np.float32)
        nir_f = nir_band.astype(np.float32)
        
        # Avoid division by zero
        denominator = nir_f + red_f
        denominator[denominator == 0] = 1e-5
        
        ndvi_map = (nir_f - red_f) / denominator
        mean_ndvi = float(np.clip(np.mean(ndvi_map), -1.0, 1.0))
        
        # Canopy cover: Pixels with healthy vegetative signature (NDVI > 0.35)
        canopy_mask = ndvi_map > 0.35
        canopy_coverage = float(np.sum(canopy_mask) / ndvi_map.size)
        
        # High-vigor clusters indicating potential weed patches
        weed_mask = ndvi_map > 0.65
        weed_density = float(np.sum(weed_mask) / ndvi_map.size)
        
        return {
            "mean_ndvi": mean_ndvi,
            "canopy_coverage": canopy_coverage,
            "weed_density": weed_density
        }

    @staticmethod
    def generate_synthetic_field_image(health_stage: str, size: int = 128) -> Tuple[np.ndarray, np.ndarray]:
        """Procedurally creates matching Synthetic RED and NIR bands for testing."""
        red = np.full((size, size), 60, dtype=np.uint8)
        nir = np.full((size, size), 80, dtype=np.uint8)
        
        if health_stage == "VIGOROUS":
            red = np.clip(red - 30 + np.random.normal(0, 5, red.shape), 0, 255).astype(np.uint8)
            nir = np.clip(nir + 100 + np.random.normal(0, 10, nir.shape), 0, 255).astype(np.uint8)
        elif health_stage == "DROUGHT_STRESSED":
            red = np.clip(red + 40 + np.random.normal(0, 5, red.shape), 0, 255).astype(np.uint8)
            nir = np.clip(nir - 20 + np.random.normal(0, 8, nir.shape), 0, 255).astype(np.uint8)
        elif health_stage == "WEED_INFESTED":
            red = np.clip(red - 20 + np.random.normal(0, 5, red.shape), 0, 255).astype(np.uint8)
            nir = np.clip(nir + 120 + np.random.normal(0, 12, nir.shape), 0, 255).astype(np.uint8)
            
        return red, nir


# -----------------------------------------------------------------------------
# 3. OUTDOOR TELEMETRY LEXICON (Grammar & Tokenizer)
# -----------------------------------------------------------------------------
class OutdoorTelemetryLexicon:
    """Encodes tabular sensor variables and visual tokens into integer sequences."""
    def __init__(self, vocab_size: int):
        self.vocab_size = vocab_size
        self.w2i = {"<PAD>": 0, "<BOS>": 1, "<EOS>": 2, "<UNK>": 3}
        self.i2w = {0: "<PAD>", 1: "<BOS>", 2: "<EOS>", 3: "<UNK>"}
        self.counter = 4

    def add_token(self, token: str):
        if token not in self.w2i and self.counter < self.vocab_size:
            self.w2i[token] = self.counter
            self.i2w[self.counter] = token
            self.counter += 1

    def encode(self, text: str, max_len: int) -> torch.Tensor:
        words = text.upper().split()
        token_ids = [self.w2i["<BOS>"]]
        
        for w in words:
            if w not in self.w2i:
                self.add_token(w)
            token_ids.append(self.w2i.get(w, self.w2i["<UNK>"]))
            
        token_ids.append(self.w2i["<EOS>"])
        
        while len(token_ids) < max_len:
            token_ids.append(self.w2i["<PAD>"])
            
        return torch.tensor(token_ids[:max_len], dtype=torch.long)

    def decode(self, token_tensor: torch.Tensor) -> str:
        tokens = [self.i2w.get(idx.item(), "<UNK>") for idx in token_tensor if idx.item() not in [0, 1, 2]]
        return " ".join(tokens)


# Quick validation check
if __name__ == "__main__":
    lexicon = OutdoorTelemetryLexicon(CONFIG.vocab_size)
    red, nir = OutdoorVisionFrontend.generate_synthetic_field_image("VIGOROUS")
    metrics = OutdoorVisionFrontend.process_multispectral_bands(red, nir)
    
    sample_telemetry = (
        f"<WEATHER> RAIN_PROB 0.20 WIND 12.4 TEMP 21.5 "
        f"<SOIL> MOIST_10CM 24.2 MOIST_40CM 28.0 NPK_N 42.0 "
        f"<VISION> NDVI {metrics['mean_ndvi']:.2f} CANOPY {metrics['canopy_coverage']:.2f} WEED {metrics['weed_density']:.2f}"
    )
    
    encoded = lexicon.encode(sample_telemetry, CONFIG.max_seq_len)
    print("Sample Telemetry String:\n", sample_telemetry)
    print("\nEncoded Tensor Shape:", encoded.shape)