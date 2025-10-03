'''
Initialize config on each program run.
Thus also allows project level config override.

config file name in JSON: 
.po.json

File format:
{
    "AI_IDENTIFIER": "/ai",
    "config": {
        "allow_context": True
    }
    "INDICATOR": "$", 
}
'''


'''
Extract all required env vars in config obj -> config.env_x_var
Do Type changing
'''
import os
import json
from pathlib import Path

class Config:
    CONFIG_FILE_NAME = ".po.json"
    
    def __init__(self):
        self.config_data = {}
        self.config_path = None
        self.load_config()
    
    def get_global_config_dir(self):
        """Get platform-specific global config directory"""
        if os.name == 'nt':  # Windows
            return Path.home() / "AppData" / "Roaming" / "po"
        else:  # Linux/macOS
            return Path.home() / ".config" / "po"
    
    def get_config_path(self):
        """Find config file: pwd first, then global, return None if not found"""
        # Check current directory first
        pwd_config = Path.cwd() / self.CONFIG_FILE_NAME
        if pwd_config.exists():
            return pwd_config
        
        # Check global config directory
        global_config = self.get_global_config_dir() / self.CONFIG_FILE_NAME
        if global_config.exists():
            return global_config
        
        return None
    
    def load_config(self):
        """Load config from file or create default"""
        self.config_path = self.get_config_path()
        
        if self.config_path:
            try:
                with open(self.config_path, 'r') as f:
                    self.config_data = json.load(f)
            except (json.JSONDecodeError, IOError) as e:
                raise ValueError(f"Error loading config from {self.config_path}: {e}")
        else:
            # No config found, create default global config
            self.create_default_global_config()
    
    def create_default_global_config(self):
        """Create default config in global directory"""
        global_config_dir = self.get_global_config_dir()
        global_config_dir.mkdir(parents=True, exist_ok=True)
        
        self.config_path = global_config_dir / self.CONFIG_FILE_NAME
        
        # Default configuration
        self.config_data = {
            "AI_IDENTIFIER": "/ai",
            "allow_context": True,
            "INDICATOR": "$"
        }
        
        self.save_config()
    
    def save_config(self):
        """Save current config to file"""
        if self.config_path:
            with open(self.config_path, 'w') as f:
                json.dump(self.config_data, f, indent=4)
    
    def get(self, key, default=None):
        """Get config value"""
        return self.config_data.get(key, default)
    
    def set(self, key, value):
        """Set config value and save"""
        self.config_data[key] = value
        self.save_config()
    
    def is_project_config(self):
        """Check if current config is project-level"""
        return self.config_path and self.config_path.parent == Path.cwd()
    
    def is_global_config(self):
        """Check if current config is global"""
        return self.config_path and self.config_path.parent == self.get_global_config_dir()

# Usage example:
# if __name__ == "__main__":
#     config = Config()
#     print(f"Config loaded from: {config.config_path}")
#     print(f"AI Identifier: {config.get('AI_IDENTIFIER')}")
#     print(f"Allow context: {config.get_nested('config', 'allow_context')}")