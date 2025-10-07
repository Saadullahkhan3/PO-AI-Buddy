'''
Initialize config on each program run.
Thus also allows project level config override.

config file name in JSON: 
.po.json
'''

DEFAULT_CONFIG = {
    "indicator": "$",
    "models": [
        {
            "alias": "gpt5",
            "provider": "openai/gpt-4"
        },
        {
            "alias": "gini",
            "provider": "google/gemini-pro"
        },
        {
            "alias": "meta",
            "provider": "meta"
        },
        {
            "alias": "ant",
            "provider": "anthropic/claude-3"
        },
        {
            "alias": "o",
            "provider": "ollama/llama3"
        },
        {
            "alias": "deep",
            "provider": "deepseek/deepseek-chat"
        },
        {
            "alias": "groq",
            "provider": "groq/llama-3.1-8b-instant"
        },
    ],
    "default_model": "groq",
    "default_model_alias": "bhai",

}


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
        # return None
        """Find config file: pwd first, then global, return None if not found"""
        # Check current directory first
        pwd_config = Path.cwd() / Config.CONFIG_FILE_NAME
        if pwd_config.exists():
            return pwd_config
        
        # Check global config directory
        global_config = self.get_global_config_dir() / Config.CONFIG_FILE_NAME
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
            print("No config found, do you want to create a global level config?")
            confirm = input("(y/n): ").lower().strip()
            if not confirm == "y":
                raise FileNotFoundError("Config file not found. Exiting.")
            self.create_default_global_config()
    

    def create_default_global_config(self):
        """Create default config in global directory"""
        global_config_dir = self.get_global_config_dir()
        global_config_dir.mkdir(parents=True, exist_ok=True)
        
        self.config_path = global_config_dir / Config.CONFIG_FILE_NAME
        
        # Default configuration
        self.config_data = DEFAULT_CONFIG
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
    

    def get_alias_and_provider(self, alias: str, include_default: bool = True) -> bool:
        """Check if a model alias exists in the config."""
        default = self.get("default_model_alias") if include_default else None
        if alias in default:
            alias = self.get("default_model")
        
        models = self.get("models", [])
        valid_alias = list(filter(lambda x: x.get("alias") == alias, models))
        if len(valid_alias) == 1:
            return valid_alias[0]["alias"], valid_alias[0]["provider"]
        else:
            return None
