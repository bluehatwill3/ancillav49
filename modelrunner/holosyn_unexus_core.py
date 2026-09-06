#!/usr/bin/env python3
import os
import sys
import re
import json
import builtins
import importlib.util
from abc import ABC, abstractmethod
from typing import Dict, Any, List

import torch
import torch.nn as nn
import numpy as np

# ==============================================================================
# 1. CORE INTERFACE & NAMESPACE BINDING
# ==============================================================================
class BaseObserver(ABC):
    """Abstract Base Class for all Holosyn Observers."""
    @abstractmethod
    def evaluate(self, s: float, sy: float, p: float, snn: Any, text: str = "", haptic_level: float = 0.0, **kwargs) -> float:
        return 0.5

# Ensure BaseObserver is globally accessible to dynamically loaded modules
setattr(builtins, "BaseObserver", BaseObserver)
sys.modules['__main__'].BaseObserver = BaseObserver

# ==============================================================================
# 2. DYNAMIC TRANSFORMER CORE
# ==============================================================================
class TransformerCore(nn.Module):
    def __init__(self, in_dim=5, h_dim=32, n_heads=2, n_layers=1, role="GENERAL"):
        super().__init__()
        self.in_dim = in_dim
        self.h_dim = h_dim
        self.role = role
        self._build_layers()
        
    def _build_layers(self):
        self.embedding = nn.Linear(self.in_dim, self.h_dim)
        self.pos_encoder = nn.Parameter(torch.zeros(1, 512, self.h_dim))
        layer = nn.TransformerEncoderLayer(d_model=self.h_dim, nhead=self.n_heads, dim_feedforward=64, batch_first=True)
        self.transformer = nn.TransformerEncoder(layer, num_layers=self.n_layers)
        self.projector = nn.Linear(self.h_dim, 1)
        
    def forward(self, x):
        return torch.tanh(self.projector(self.transformer(self.embedding(x)).mean(dim=1)))
        
    def assimilate(self, w_obj):
        try:
            state = w_obj.state_dict() if hasattr(w_obj, 'state_dict') else w_obj
            self.load_state_dict({k: v for k, v in state.items() if isinstance(v, torch.Tensor)}, strict=False)
        except Exception as e:
            print(f"   [Assimilator] Skip layer: {e}")

# ==============================================================================
# 3. NEXUS ENGINE: VAULT LOADER & OBSERVER SWARM
# ==============================================================================
class HolosynNexusEngine:
    def __init__(self, primary_vault="/home/devcbloom"):
        self.primary_vault = primary_vault
        self.observers: Dict[str, BaseObserver] = {}
        self.cores = nn.ModuleDict({"FOUNDATION": TransformerCore()})
        
        # Trigger initial recursive vault search
        self.rebuild_manifold(self.primary_vault)

    def load_observer_plugin(self, path: str):
        """Manually or automatically ingest .py files and activate observers."""
        if os.path.isdir(path):
            print(f"   📂 INGESTING DIRECTORY: {path}")
            for root, _, files in os.walk(path):
                for file in files:
                    if file.endswith(".py"):
                        self._process_python_file(os.path.join(root, file))
        else:
            self._process_python_file(path)

    def _process_python_file(self, file_path: str):
        module_name = f"plugin_{os.path.basename(file_path).split('.')[0]}"
        try:
            spec = importlib.util.spec_from_file_location(module_name, file_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            
            found = False
            for attr in dir(module):
                obj = getattr(module, attr)
                if isinstance(obj, type) and issubclass(obj, BaseObserver) and obj is not BaseObserver:
                    self.observers[attr[:3].upper()] = obj()
                    print(f"   ✅ ACTIVATED OBSERVER: {attr}")
                    found = True
            if not found:
                print(f"   ⚠️ No valid BaseObserver subclasses found in: {file_path}")
        except Exception as e:
            print(f"   ❌ PLUGIN FAULT: {e}")

    def rebuild_manifold(self, path: str):
        """Recursive search for .pt files in /home/devcbloom."""
        if not os.path.exists(path):
            return
            
        print(f"\n[Vault] Recursive harvest: {path}")
        for root, _, files in os.walk(path):
            for file in files:
                if file.endswith((".pt", ".pth", ".bin")):
                    try:
                        weights = torch.load(os.path.join(root, file), map_location='cpu', weights_only=False)
                        core_id = re.sub(r'[^A-Z0-9_]', '_', file.split('.')[0].upper())
                        if core_id not in self.cores:
                            self.cores[core_id] = TransformerCore(role=core_id)
                        self.cores[core_id].assimilate(weights)
                        print(f"   📦 INGESTED WEIGHTS: {file}")
                    except:
                        pass
                elif file.endswith(".py"):
                    self.load_observer_plugin(os.path.join(root, file))

# ==============================================================================
# 4. EXECUTION INTERFACE
# ==============================================================================
if __name__ == "__main__":
    print("💠 INITIALIZING HOLOSYN NEXUS 💠")
    nexus = HolosynNexusEngine(primary_vault="/home/devcbloom")
    
    # Manual Trigger Example for custom directory:
    # nexus.load_observer_plugin("./custom_plugins")
    
    print("\n[Status] Engine ready. System awaiting input...")