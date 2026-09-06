#!/usr/bin/env python3
import os
import sys
import re
import importlib.util
from abc import ABC, abstractmethod
from typing import Dict, List, Any
import builtins
import torch
import torch.nn as nn
import numpy as np

# ==============================================================================
# 1. CORE INTERFACE & NAMESPACE BINDING
# ==============================================================================

class BaseObserver(ABC):
    """
    Abstract Base Class for all Holosyn Observers.
    """
    @abstractmethod
    def evaluate(self, s: float, sy: float, p: float, snn: Any, text: str = "", haptic_level: float = 0.0, **kwargs) -> float:
        return 0.5

# CRITICAL: Expose BaseObserver globally. This prevents the "No valid BaseObserver subclasses" fault.
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
# 3. NEXUS ENGINE: ULTRA VAULT LOADER
# ==============================================================================

class HolosynNexusEngine:
    def __init__(self, primary_vault: str = "/home/devcbloom"):
        self.observers: Dict[str, BaseObserver] = {}
        self.cores = nn.ModuleDict({"FOUNDATION": TransformerCore()})
        
        # Trigger initial recursive vault search
        if os.path.exists(primary_vault):
            self.harvest_workspace(primary_vault)
        else:
            print(f"[Warning] Vault path '{primary_vault}' is missing.")

    def harvest_workspace(self, base_path: str):
        """Recursive crawler for .pt tensors and .py observers."""
        print(f"\n[Nexus] Recursive scan initiated: {base_path}")
        for root, _, files in os.walk(base_path):
            for file in files:
                full_path = os.path.join(root, file)
                if file.endswith((".pt", ".pth", ".bin")):
                    self._ingest_tensor(full_path, file)
                elif file.endswith(".py"):
                    self.load_observer_plugin(full_path)

    def _ingest_tensor(self, path: str, filename: str):
        try:
            weights = torch.load(path, map_location='cpu', weights_only=False)
            core_id = re.sub(r'[^A-Z0-9_]', '_', filename.split('.')[0].upper())
            if core_id not in self.cores:
                self.cores[core_id] = TransformerCore(role=core_id)
            self.cores[core_id].assimilate(weights)
            print(f"   📦 INGESTED WEIGHTS: {filename}")
        except Exception as e:
            print(f"   ⚠️ TENSOR FAULT: {filename} -> {e}")

    def load_observer_plugin(self, file_path: str):
        """Dynamically ingests a python plugin or recursively sweeps a directory."""
        if os.path.isdir(file_path):
            print(f"   📂 MANUALLY INGESTING DIRECTORY: {file_path}")
            for root, _, files in os.walk(file_path):
                for file in files:
                    if file.endswith(".py"):
                        self.load_observer_plugin(os.path.join(root, file))
            return

        module_name = f"plugin_{os.path.basename(file_path).split('.')[0]}"
        try:
            spec = importlib.util.spec_from_file_location(module_name, file_path)
            if spec and spec.loader:
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                
                count = 0
                for attr in dir(module):
                    obj = getattr(module, attr)
                    if isinstance(obj, type) and issubclass(obj, BaseObserver) and obj is not BaseObserver:
                        self.observers[attr[:3].upper()] = obj()
                        print(f"   ✅ ACTIVATED OBSERVER: {attr}")
                        count += 1
                if count == 0:
                    print(f"   ⚠️ No valid BaseObserver subclasses in: {file_path}")
        except Exception as e:
            print(f"   ❌ PLUGIN FAULT: {e}")

# ==============================================================================
# 4. RUNTIME INTERFACE
# ==============================================================================
if __name__ == "__main__":
    print("💠 HOLOSYN NEXUS ENGINE ACTIVATED 💠")
    nexus = HolosynNexusEngine(primary_vault="/home/devcbloom")
    
    print("\n[Commands] /vault <path> | /plugin <path> | /quit")
    while True:
        try:
            cmd = input("\n[OMNI NEXUS] > ").strip()
            if cmd == "/quit": break
            
            if cmd.startswith("/vault "):
                nexus.harvest_workspace(cmd.split(" ")[1])
            elif cmd.startswith("/plugin "):
                nexus.load_observer_plugin(cmd.split(" ")[1])
            else:
                print(f"[Engine] Passive mode. Ready for telemetry.")
        except KeyboardInterrupt:
            break