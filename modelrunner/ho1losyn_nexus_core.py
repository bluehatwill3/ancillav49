#!/usr/bin/env python3
import os
import sys
import importlib.util
import builtins
import re
from abc import ABC, abstractmethod
from typing import Dict, Any

import torch
import torch.nn as nn
import numpy as np

# ==============================================================================
# 1. GLOBAL SCOPE OBSERVER INTERFACE (Namespace Locked)
# ==============================================================================

class BaseObserver(ABC):
    """
    Abstract Base Class for all Holosyn Observers.
    """
    @abstractmethod
    def evaluate(self, s: float, sy: float, p: float, snn: Any, text: str = "", haptic_level: float = 0.0, **kwargs) -> float:
        return 0.5

# CRITICAL: Force BaseObserver into builtins so all dynamic plugins see the exact same class
setattr(builtins, "BaseObserver", BaseObserver)
sys.modules['__main__'].BaseObserver = BaseObserver

# ==============================================================================
# 2. DYNAMIC TRANSFORMER CORE
# ==============================================================================

class TransformerCore(nn.Module):
    def __init__(self, role="GENERAL"):
        super().__init__()
        self.role = role
        self.embedding = nn.Linear(5, 32)
        self.projector = nn.Linear(32, 1)
        
    def forward(self, x):
        return torch.tanh(self.projector(self.embedding(x).mean(dim=1)))
        
    def assimilate(self, w_obj):
        try:
            state = w_obj.state_dict() if hasattr(w_obj, 'state_dict') else w_obj
            self.load_state_dict({k: v for k, v in state.items() if isinstance(v, torch.Tensor)}, strict=False)
        except Exception:
            pass

# ==============================================================================
# 3. NEXUS ENGINE: VAULT LOADER & OBSERVER SWARM
# ==============================================================================

class HolosynNexusEngine:
    def __init__(self, primary_vault: str = "/home/devcbloom"):
        self.observers: Dict[str, BaseObserver] = {}
        self.cores = nn.ModuleDict({"FOUNDATION": TransformerCore()})
        
        # Trigger initial scan
        if os.path.exists(primary_vault):
            self.harvest_workspace(primary_vault)
        else:
            print(f"[Warning] Vault path '{primary_vault}' is missing.")

    def harvest_workspace(self, base_path: str):
        """Recursively parses vault directories to ingest state tensors (.pt) and plugins (.py)."""
        print(f"\n[Nexus] Recursive harvest initiated: {base_path}")
        
        for root, _, files in os.walk(base_path):
            for file in files:
                full_path = os.path.join(root, file)
                
                # Ingest .py plugins
                if file.endswith(".py"):
                    self.load_observer_plugin(full_path)
                    
                # Ingest .pt neural weight checkpoints
                elif file.endswith((".pt", ".pth", ".bin")):
                    try:
                        weights = torch.load(full_path, map_location='cpu', weights_only=False)
                        core_id = re.sub(r'[^A-Z0-9_]', '_', file.split('.')[0].upper())
                        if core_id not in self.cores:
                            self.cores[core_id] = TransformerCore(role=core_id)
                        self.cores[core_id].assimilate(weights)
                        print(f"   📦 INGESTED TENSOR MATRIX: {file}")
                    except Exception as e:
                        print(f"   ⚠️ TENSOR EXTRACTION VARIANCE: {file} -> {e}")

    def load_observer_plugin(self, file_path: str):
        """Dynamically loads .py files and activates valid BaseObserver instances."""
        if os.path.isdir(file_path):
            print(f"   📂 INGESTING PLUGIN DIRECTORY: {file_path}")
            for root, _, files in os.walk(file_path):
                for file in files:
                    if file.endswith(".py"):
                        self.load_observer_plugin(os.path.join(root, file))
            return

        module_name = f"plugin_{os.path.basename(file_path).split('.')[0]}"
        try:
            spec = importlib.util.spec_from_file_location(module_name, file_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            
            found_count = 0
            for attr in dir(module):
                obj = getattr(module, attr)
                # Verify inheritance from the globally injected BaseObserver
                if isinstance(obj, type) and issubclass(obj, BaseObserver) and obj is not BaseObserver:
                    obs_key = attr[:3].upper()
                    self.observers[obs_key] = obj()
                    print(f"   ✅ ACTIVATED OBSERVER: '{obs_key}' ({attr})")
                    found_count += 1
            
            if found_count == 0:
                print(f"   ⚠️ No valid BaseObserver subclasses found in: {file_path}")
                
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
                nexus.harvest_workspace(cmd.split(" ", 1)[1])
            elif cmd.startswith("/plugin "):
                nexus.load_observer_plugin(cmd.split(" ", 1)[1])
            else:
                print(f"[Engine] Passive mode. Ready for telemetry.")
                
        except KeyboardInterrupt:
            break