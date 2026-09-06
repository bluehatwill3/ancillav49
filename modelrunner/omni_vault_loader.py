#!/usr/bin/env python3
"""
HOLOSYN OMNI-VAULT NEXUS PLUGIN
================================================================
A Meta-Observer that automatically scans its local directory, 
instantiates all compatible Holosyn observers, and aggregates 
their outputs into a unified cognitive consensus vector.

WARNING: If scanning a directory containing multiple heavy ML 
models (e.g., hf_slm, hf_mega_nexus), monitor local VRAM closely.
"""

import os
import sys
import importlib.util
import inspect
import numpy as np

# ---------------------------------------------------------
# 🔌 DYNAMIC WORKSPACE COMPATIBILITY BRIDGE
# ---------------------------------------------------------
try:
    BaseObserver = sys.modules['__main__'].BaseObserver
except (KeyError, AttributeError):
    class BaseObserver:
        """Fallback framework for standard decoupled terminal environments."""
        def evaluate(self, s, sy, p, snn, text="", haptic_level=0.0, **kwargs): 
            return 0.5

# ---------------------------------------------------------
# 🌐 THE DIRECTORY META-OBSERVER
# ---------------------------------------------------------
class OmniDirectoryNexus(BaseObserver):
    def __init__(self, target_dir="."):
        super().__init__()
        self.target_dir = target_dir
        self.active_sub_observers = {}
        self.history = []
        self._harvest_directory()

    def _harvest_directory(self):
        """Scans the designated directory and dynamically boots all compatible observer classes."""
        print(f"💠 [OMNI-NEXUS] Initiating Directory Sweep in: {os.path.abspath(self.target_dir)}")
        current_file = os.path.basename(__file__)

        # Files to explicitly ignore (not observers)
        ignore_list = [current_file, "core_forge.py", "__init__.py"]

        for filename in os.listdir(self.target_dir):
            if not filename.endswith(".py") or filename in ignore_list:
                continue

            filepath = os.path.join(self.target_dir, filename)
            try:
                # 1. Dynamically load the module directly from the file path
                spec = importlib.util.spec_from_file_location(filename[:-3], filepath)
                if spec is None: 
                    continue
                module = importlib.util.module_from_spec(spec)
                
                # Prevent stdout spam from sub-modules during import
                spec.loader.exec_module(module)

                # 2. Inspect the module for valid Observer Classes
                for name, obj in inspect.getmembers(module, inspect.isclass):
                    # Skip the fallback BaseObserver class itself to prevent empty loops
                    if name == "BaseObserver":
                        continue
                    
                    # Identify classes by checking if they possess a callable 'evaluate' method
                    if hasattr(obj, 'evaluate') and callable(getattr(obj, 'evaluate')):
                        print(f"   🔌 Booting Component: {name} (via {filename})")
                        try:
                            # Instantiate the sub-observer and store it
                            instance = obj()
                            self.active_sub_observers[name] = instance
                        except Exception as e:
                            print(f"   ❌ Failed to initialize '{name}': {e}")

            except Exception as e:
                print(f"   ⚠️ Module Failure - Could not process '{filename}': {e}")

        print(f"✅ [OMNI-NEXUS] Directory sweep complete. Active Observer Core Count: {len(self.active_sub_observers)}\n")

    def evaluate(self, s, sy, p, snn, text="", haptic_level=0.0, **kwargs):
        """
        Routes the sensory execution states through every single harvested sub-observer
        and aggregates their floating metric returns into a single consensus array.
        """
        if not self.active_sub_observers:
            return 0.5  # Neutral baseline if the directory was empty

        consensus_scores = []
        
        # Poll every booted observer
        for name, observer_instance in self.active_sub_observers.items():
            try:
                score = observer_instance.evaluate(
                    s=s, sy=sy, p=p, snn=snn, text=text, 
                    haptic_level=haptic_level, **kwargs
                )
                consensus_scores.append(score)
            except Exception as e:
                # Silent failsafe: If a single plugin crashes mid-evaluation 
                # (e.g., an ML model OOM error), it will not crash the master loop.
                pass

        if not consensus_scores:
            return 0.52

        # Calculate the mathematical mean across all successful observer states
        final_meta_score = float(np.mean(consensus_scores))

        self.history.append(final_meta_score)
        if len(self.history) > 100:
            self.history.pop(0)

        return float(final_meta_score)

# ---------------------------------------------------------
# 🔨 STANDALONE TESTING
# ---------------------------------------------------------
if __name__ == "__main__":
    print("💠 INITIALIZING STANDALONE DIRECTORY SWEEP 💠")
    
    # Instantiate the Nexus (Will automatically scan the folder it is placed in)
    omni_nexus = OmniDirectoryNexus()
    
    # Generate mock states
    mock_snn_states = [0.45, 0.66, 0.12, 0.88]
    mock_img = np.random.randint(0, 255, (224, 224, 3), dtype=np.uint8)

    # Fire an evaluation loop
    result = omni_nexus.evaluate(
        s=0.75, sy=0.80, p=0.65, snn=mock_snn_states,
        text="Initiating global observer consensus protocol.",
        image=mock_img
    )
    
    print("═" * 70)
    print(f"📡 FINAL AGGREGATED OMNI-RESONANCE VECTOR: {result:.4f}")
    print("═" * 70)