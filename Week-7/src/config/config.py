import yaml
import os
from pathlib import Path
from typing import Dict, Any

class Config:
    def __init__(self, env: str = "dev"):
        config_file = f"config.{env}.yaml"
        config_path = Path(__file__).parent / config_file
        
        if not config_path.exists():
            raise FileNotFoundError(f"Config file not found: {config_path}")
        
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)
        self.env = env
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get nested config value using dot notation"""
        keys = key.split('.')
        value = self.config
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
            else:
                return default
        return value if value is not None else default
    
    @property
    def index_path(self) -> Path:
        return Path(self.config['paths']['index_file'])
    
    @property
    def metadata_path(self) -> Path:
        return Path(self.config['paths']['metadata_file'])
    
    @property
    def images_dir(self) -> Path:
        return Path(self.config['paths']['images_dir'])
    
    @property
    def logs_dir(self) -> Path:
        return Path(self.config['paths']['logs_dir'])
    
    @property
    def model_name(self) -> str:
        return self.config['model']['name']
    
    @property
    def embedding_model(self) -> str:
        return self.config['embeddings']['model']
    
    @property
    def db_path(self) -> Path:
        return Path(self.config['database']['path'])

# Global config instance
_config = None

def get_config(env: str = None) -> Config:
    global _config
    if _config is None:
        env = env or os.getenv('APP_ENV', 'dev')
        _config = Config(env)
    return _config

def reset_config():
    global _config
    _config = None