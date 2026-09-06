import os
import time
import importlib.util
import inspect
import torch
from abc import ABC, abstractmethod
from typing import Dict, Any, List

# ==========================================
# 1. Base Architecture
# ==========================================
class BaseObserver(ABC):
    """
    The strict contract for all plugins in the ecosystem.
    """
    @abstractmethod
    def update(self, event_type: str, event_data: Dict[str, Any]):
        pass

# ==========================================
# 2. Automatic Plugin Manager
# ==========================================
class PluginManager:
    """
    Dynamically discovers and loads plugins to keep the system autonomous.
    """
    def __init__(self, plugin_dir: str = "."):
        self.plugin_dir = plugin_dir
        self.observers: List[BaseObserver] = []

    def load_plugins(self):
        """Scans the directory for valid BaseObserver subclasses."""
        for filename in os.listdir(self.plugin_dir):
            if filename.endswith(".py") and filename != __file__:
                module_name = filename[:-3]
                file_path = os.path.join(self.plugin_dir, filename)
                
                # Dynamically load the module
                spec = importlib.util.spec_from_file_location(module_name, file_path)
                if spec and spec.loader:
                    module = importlib.util.module_from_spec(spec)
                    try:
                        spec.loader.exec_module(module)
                        self._register_classes_from_module(module)
                    except Exception as e:
                        print(f"[Debugger] Fault loading plugin {filename}: {e}")

    def _register_classes_from_module(self, module):
        """Finds and instantiates valid observers."""
        for name, obj in inspect.getmembers(module, inspect.isclass):
            if issubclass(obj, BaseObserver) and obj is not BaseObserver:
                print(f"[PluginManager] Automatically loaded and registered: {name}")
                self.observers.append(obj())

    def broadcast(self, event_type: str, event_data: Dict[str, Any]):
        """Sends events to all organically loaded plugins."""
        for observer in self.observers:
            try:
                observer.update(event_type, event_data)
            except Exception as e:
                print(f"[Debugger] Plugin {observer.__class__.__name__} failed during update: {e}")

# ==========================================
# 3. Vault Loader and Debugger
# ==========================================
class VaultLoaderDebugger:
    """
    Monitors the external NTFS storage vault and triggers organic learning.
    """
    def __init__(self, plugin_manager: PluginManager, mount_path: str = "/mnt/holosyn_archive"):
        self.mount_path = mount_path
        self.plugin_manager = plugin_manager
        
        # Files to monitor for organic growth
        self.target_manifolds = [
            "best_manifold(2).pt",  #
            "latest_manifold(1).pt" #
        ]
        self.last_modified_times = {file: 0.0 for file in self.target_manifolds}

    def verify_vault_connection(self) -> bool:
        """Ensures the /dev/sdc1 NTFS drive is accessible."""
        if not os.path.exists(self.mount_path):
            print(f"[Debugger Error] Vault not accessible at {self.mount_path}. Check /dev/sdc1 mounting.")
            return False
        return True

    def scan_vault(self):
        """Scans the vault for updated manifolds and triggers learning."""
        if not self.verify_vault_connection():
            return

        for manifold_file in self.target_manifolds:
            file_path = os.path.join(self.mount_path, manifold_file)
            
            if os.path.exists(file_path):
                current_mtime = os.path.getmtime(file_path)
                
                # If the file is new or has been updated
                if current_mtime > self.last_modified_times[manifold_file]:
                    print(f"[Vault Loader] New data detected in {manifold_file}. Initiating organic learning phase...")
                    self.last_modified_times[manifold_file] = current_mtime
                    
                    self._process_manifold(file_path, manifold_file)

    def _process_manifold(self, file_path: str, filename: str):
        """Loads the manifold into memory and broadcasts to plugins."""
        try:
            # Assuming these are standard serialized state dictionaries[cite: 14, 15]
            state_data = torch.load(file_path, map_location=torch.device('cpu'))
            
            # Broadcast the loaded manifold to all autonomous plugins
            self.plugin_manager.broadcast("MANIFOLD_UPDATED", {
                "filename": filename,
                "state_data": state_data,
                "timestamp": time.time()
            })
            print(f"[Debugger] Successfully broadcasted {filename} to all active neural/quantum plugins.")
            
        except Exception as e:
            print(f"[Debugger Fault] Corruption or read error in {filename}: {e}")

# ==========================================
# Main Autonomous Loop
# ==========================================
def run_autonomous_loop():
    print("Starting Autonomous Holosyn Ecosystem...")
    
    manager = PluginManager()
    # Scans the current directory for any system modifiers or model plugins
    manager.load_plugins() 
    
    vault = VaultLoaderDebugger(manager)
    
    try:
        while True:
            # Continuously monitor the vault for organic updates
            vault.scan_vault()
            time.sleep(10) # Poll every 10 seconds
    except KeyboardInterrupt:
        print("\n[System] Autonomous subconscious halted by user.")

if __name__ == "__main__":
    run_autonomous_loop()