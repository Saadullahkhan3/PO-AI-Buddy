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
            "alias": "bro",
            "provider": "groq/llama-3.3-70b-versatile"
        },
        {
            "alias": "groq",
            "provider": "groq/llama-3.1-8b-instant"
        },
        {
            "alias": "own",
            "provider": "ollama//models/Llama-3.2-3B-Instruct-Q4_K_M.gguf",
            "base_url": "http://158.101.98.132:9090/"
        }
    ],
    "default_model": "groq",
    "default_model_alias": "bhai"
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
                # exit_with_error(f"Error loading config from {self.config_path}: {e}")
        else:
            print("No config found, do you want to create a global level config?")
            confirm = input("(y/n): ").lower().strip()
            if not confirm == "y":
                # exit_with_error(f"Config file not found. Exiting.")
                raise FileNotFoundError("Config file not found. Exiting.")
            self.create_default_global_config(show_dir=True)
    

    def create_default_global_config(self, show_dir=False):
        """Create default config in global directory"""
        global_config_dir = self.get_global_config_dir()
        global_config_dir.mkdir(parents=True, exist_ok=True)
        
        self.config_path = global_config_dir / Config.CONFIG_FILE_NAME
        
        # Default configuration
        self.config_data = DEFAULT_CONFIG
        print(f"Config File has been created at:\n{self.config_path} \nMake sure to customize it :)") if show_dir else None
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
    

    def get_alias_and_provider(self, alias: str) -> tuple[str | None, str | None]:
        """Get alias, provider, and base_url for a given alias, with fallback to default."""
        default_alias_keyword = self.get("default_model_alias")
        
        # If user typed the default alias keyword (e.g., "bhai"), resolve to actual default model
        if alias == default_alias_keyword:
            alias = self.get("default_model")
        
        models = self.get("models", [])
        
        # Try to find the requested alias
        valid_alias = list(filter(lambda x: x.get("alias") == alias, models))
        if len(valid_alias) == 1:
            model = valid_alias[0]
            return model.get("alias"), model.get("provider"), model.get("base_url")
        
        # Alias not found, try to use the default model as fallback
        default_model = self.get("default_model")
        matched_default = list(filter(lambda x: x.get("alias") == default_model, models))
        
        if len(matched_default) == 1:
            model = matched_default[0]
            return default_model, model.get("provider"), model.get("base_url")
        
        # No valid alias or default found
        return None, None, None

