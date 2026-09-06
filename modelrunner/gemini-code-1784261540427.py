import json
import os
import shutil

class SystemModifier:
    """
    API for managing system configurations and environment settings.
    """
    def __init__(self, config_path="config.json"):
        self.config_path = config_path

    def update_config(self, key, value):
        """Updates a specific configuration key in your local JSON config."""
        config = {}
        if os.path.exists(self.config_path):
            with open(self.config_path, 'r') as f:
                config = json.load(f)
        
        config[key] = value
        
        with open(self.config_path, 'w') as f:
            json.dump(config, f, indent=4)
        return f"Config updated: {key} -> {value}"

    def set_env_variable(self, var_name, value):
        """Safely sets an environment variable for the current process."""
        os.environ[var_name] = str(value)
        return f"Environment variable {var_name} set."