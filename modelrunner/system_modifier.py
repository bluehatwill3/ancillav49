import json
import os
from abc import ABC, abstractmethod
from typing import Any, Dict

# ==========================================
# 1. Base Observer Definition
# ==========================================
class BaseObserver(ABC):
    """
    Abstract base class that all Holosyn system plugins must inherit from.
    This resolves the 'No valid BaseObserver subclasses found' fault.
    """
    @abstractmethod
    def update(self, event_type: str, event_data: Dict[str, Any]):
        """
        Receives updates from the main autonomous system loop.
        """
        pass

# ==========================================
# 2. System Modifier Plugin Implementation
# ==========================================
class SystemModifier(BaseObserver):
    """
    Plugin to manage system configurations and monitor data ingestion.
    """
    def __init__(self, config_path: str = "config.json"):
        self.config_path = config_path
        self._ensure_config_exists()

    def _ensure_config_exists(self):
        """Creates a default configuration file if one does not exist."""
        if not os.path.exists(self.config_path):
            with open(self.config_path, 'w') as f:
                json.dump({"status": "initialized", "last_event": None}, f, indent=4)

    def update(self, event_type: str, event_data: Dict[str, Any]):
        """
        Implementation of the BaseObserver update method.
        Listens for dataset loading or system faults.
        """
        print(f"[SystemModifier] Event Intercepted: {event_type}")
        
        # Example logic: Log the event to the system config
        self.modify_config("last_event", event_type)
        
        if event_type == "DATASET_LOADED":
            print(f"[SystemModifier] Acknowledged loading of {len(event_data.get('dataset', []))} items.")

    def modify_config(self, key: str, value: Any):
        """
        Safely modifies local configuration parameters dynamically.
        """
        try:
            with open(self.config_path, 'r') as f:
                config = json.load(f)
                
            config[key] = value
            
            with open(self.config_path, 'w') as f:
                json.dump(config, f, indent=4)
                
            print(f"[SystemModifier] Successfully updated config: {key} -> {value}")
        except Exception as e:
            print(f"[SystemModifier] Error modifying config: {e}")

# Example local execution/testing block
if __name__ == "__main__":
    # Test to ensure the module runs without faults
    plugin = SystemModifier()
    plugin.update("TEST_FAULT_RESOLUTION", {"status": "success"})