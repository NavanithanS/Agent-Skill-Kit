import yaml
from pathlib import Path
from typing import Dict, Any

CONFIG_PATH = Path.home() / ".askconfig.yaml"

def load_config() -> Dict[str, Any]:
    """
    Load configuration from ~/.askconfig.yaml.
    
    Returns:
        Dict: Configuration dictionary, or empty dict if not found/error.
    """
    if not CONFIG_PATH.exists():
        return {}
        
    try:
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            config = yaml.safe_load(f)
            return config or {}
    except Exception:
        return {}

def get_config_value(key: str, default: Any = None) -> Any:
    """
    Get a value from the configuration.
    Supports nested keys with dot notation (e.g. 'defaults.agent').
    """
    config = load_config()
    
    keys = key.split(".")
    value = config
    
    for k in keys:
        if isinstance(value, dict):
            value = value.get(k)
        else:
            return default
            
    return value if value is not None else default
