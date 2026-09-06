import os
import sys
import importlib.util
import inspect
from abc import ABC, abstractmethod
from typing import Dict, List, Any, Type

# ==========================================
# 1. CORE ARCHITECTURE INTERFACES
# ==========================================

class BaseObserver(ABC):
    """
    Abstract base class for all Holosyn plugins. 
    Every valid plugin file must contain a subclass inheriting from this class.
    """
    @abstractmethod
    def update(self, event_type: str, event_data: Dict[str, Any]) -> None:
        """
        Processes broadcasted events from the central core system loop.
        """
        pass


class HolosynEventHub:
    """
    Manages the live registration and broadcasting of activated observers.
    """
    def __init__(self):
        self._observers: List[BaseObserver] = []

    def register_observer(self, observer: BaseObserver) -> None:
        """Adds a verified observer instance to the live event loop."""
        if observer not in self._observers:
            self._observers.append(observer)
            print(f"[Core] Activated Observer: {observer.__class__.__name__}")

    def broadcast(self, event_type: str, event_data: Dict[str, Any]) -> None:
        """Dispatches telemetry data to all active plugins simultaneously."""
        for observer in self._observers:
            try:
                observer.update(event_type, event_data)
            except Exception as e:
                print(f"[Error] Failed broadcasting to {observer.__class__.__name__}: {e}")


# ==========================================
# 2. DYNAMIC PLUGIN LOADER
# ==========================================

class AutonomousPluginLoader:
    """
    Scans directories, safely imports .py files, analyzes classes via AST/Inspection,
    and isolates valid BaseObserver plugins.
    """
    def __init__(self, event_hub: HolosynEventHub):
        self.event_hub = event_hub

    def load_plugin_file(self, file_path: str) -> None:
        """
        Loads a single Python file, looks for BaseObserver subclasses,
        and automatically activates them.
        """
        file_path = os.path.abspath(file_path)
        if not os.path.exists(file_path):
            print(f"[Loader Error] Target file not found: {file_path}")
            return

        module_name = os.path.splitext(os.path.basename(file_path))[0]

        # Create module spec and load it into memory safely
        spec = importlib.util.spec_from_file_location(module_name, file_path)
        if spec is None or spec.loader is None:
            print(f"[Loader Error] Could not generate module spec for {file_path}")
            return

        module = importlib.util.module_from_spec(spec)
        # Append path to handle internal relative module imports cleanly
        sys.path.insert(0, os.path.dirname(file_path))

        try:
            spec.loader.exec_module(module)
            
            valid_subclass_found = False
            # Inspect all classes defined inside the loaded module
            for name, obj in inspect.getmembers(module, inspect.isclass):
                # Ensure class inherits from BaseObserver and is not the base class itself
                if issubclass(obj, BaseObserver) and obj is not BaseObserver:
                    # Instantiate the plugin and register it to the hub
                    observer_instance = obj()
                    self.event_hub.register_observer(observer_instance)
                    valid_subclass_found = True

            if not valid_subclass_found:
                print(f"[Warning] No valid BaseObserver subclasses found in target plugin file: {file_path}")

        except Exception as e:
            print(f"[Plugin Fault] Critical failure parsing module {module_name}: {e}")
        finally:
            # Clean up the path environment
            if sys.path[0] == os.path.dirname(file_path):
                sys.path.pop(0)

    def scan_directory(self, target_directory: str) -> None:
        """Scans an entire folder path for standalone plugin files."""
        if not os.path.exists(target_directory):
            print(f"[Loader Error] Directory path missing: {target_directory}")
            return

        print(f"[Loader] Scanning directory '{target_directory}' for plugins...")
        for file in os.listdir(target_directory):
            if file.endswith(".py") and file != "__init__.py":
                full_path = os.path.join(target_directory, file)
                self.load_plugin_file(full_path)


# ==========================================
# 3. VERIFICATION EXECUTION ENVIRONMENT
# ==========================================

if __name__ == "__main__":
    print("[Ecosystem] Initializing Holosyn Core Core Engine...")
    
    # Initialize Core Hub and Autonomous Loader
    hub = HolosynEventHub()
    loader = AutonomousPluginLoader(hub)

    # Creating a simulated mock plugin folder to verify loading properties
    mock_dir = "./holosyn_plugins"
    os.makedirs(mock_dir, exist_ok=True)
    
    mock_plugin_path = os.path.join(mock_dir, "system_modifier.py")
    
    # Write a dynamically valid template file into the path
    print("[Simulation] Creating standardized 'system_modifier.py' template...")
    with open(mock_plugin_path, "w") as f:
        f.write('''from holosyn_core import BaseObserver
from typing import Dict, Any

class SystemModifier(BaseObserver):
    def __init__(self):
        self.identity = "SystemModifier_V41"

    def update(self, event_type: str, event_data: Dict[str, Any]) -> None:
        print(f"[{self.identity}] Intercepted broadcast event -> Type: {event_type}")
        if "annotated_formula" in event_data:
            print(f"[{self.identity}] Telemetry Formula Parsed: {event_data['annotated_formula']}")
''')

    # Execute dynamic directory load and activate observers
    loader.scan_directory(mock_dir)

    # Test the broadcast pipeline using mathematical data metrics
    sample_telemetry = {
        "annotated_formula": "add(add(divide(1000, const_10), multiply(subtract(const_10, 1), const_10)), const_2)",
        "category": "general"
    }
    
    print("\n[Simulation] Broadcasting live dataset telemetry...")
    hub.broadcast("DATASET_INGESTION_METRIC", sample_telemetry)