#!/usr/bin/env python3
import os
import sys
import re
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
    """
    Abstract Base Class for all Holosyn Observers.
    """
    @abstractmethod
    def evaluate(self, s: float, sy: float, p: float, snn: Any, text: str = "", haptic_level: float = 0.0, **kwargs) -> float:
        return 0.5

# CRITICAL: Force BaseObserver into builtins so all dynamic plugins see the same class
setattr(builtins, "BaseObserver", BaseObserver)
sys.modules['__main__'].BaseObserver = BaseObserver


# ==============================================================================
# 2. NEXUS ENGINE: VAULT LOADER & OBSERVER SWARM
# ==============================================================================

class HolosynNexusEngine:
    def __init__(self, primary_vault: str = "/home/devcbloom"):
        self.observers: Dict[str, BaseObserver] = {}
        # Recursive scan of your dev folder upon init
        if os.path.exists(primary_vault):
            self.harvest_workspace(primary_vault)
        else:
            print(f"[Warning] Vault path '{primary_vault}' not found.")

    def harvest_workspace(self, base_path: str):
        """Recursively parses vault directories to ingest state tensors (.pt) and plugins (.py)."""
        print(f"\n[Nexus] Recursive scan initiated: {base_path}")
        
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
                        print(f"   📦 INGESTED TENSOR MATRIX: {file}")
                    except Exception as e:
                        print(f"   ⚠️ TENSOR EXTRACTION VARIANCE: {file} -> {e}")

    def load_observer_plugin(self, file_path: str):
        """Dynamically loads .py files and activates valid BaseObserver instances."""
        module_name = f"plugin_{os.path.basename(file_path).replace('.py', '')}"
        try:
            spec = importlib.util.spec_from_file_location(module_name, file_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            
            found_count = 0
            for attr in dir(module):
                obj = getattr(module, attr)
                # Verify inheritance from global BaseObserver
                if isinstance(obj, type) and issubclass(obj, BaseObserver) and obj is not BaseObserver:
                    obs_key = attr[:3].upper()
                    self.observers[obs_key] = obj()
                    print(f"   ✅ ACTIVATED OBSERVER: '{obs_key}' derived from {attr}")
                    found_count += 1
            
            if found_count == 0:
                print(f"   ⚠️ No valid BaseObserver subclasses found in: {file_path}")
                
        except Exception as e:
            print(f"   ❌ PLUGIN FAULT: {e}")

# ==============================================================================
# 3. RUNTIME INTERFACE
# ==============================================================================

if __name__ == "__main__":
    print("💠 HOLOSYN NEXUS ENGINE ACTIVATED 💠")
    nexus = HolosynNexusEngine(primary_vault="/home/devcbloom")
    
    print("\n[Status] System ready. Commands: /vault <path>, /plugin <path>, /quit")
    
    while True:
        try:
            cmd = input("\n[OMNI NEXUS] > ").strip()
            if cmd == "/quit": break
            
            parts = cmd.split(" ", 1)
            cmd_base = parts[0]
            cmd_arg = parts[1] if len(parts) > 1 else ""
            
            if cmd_base == "/vault":
                nexus.harvest_workspace(cmd_arg or "/home/devcbloom")
            elif cmd_base == "/plugin":
                nexus.load_observer_plugin(cmd_arg)
            else:
                print(f"[Engine] Input processed: {cmd}")
                
        except KeyboardInterrupt:
            break