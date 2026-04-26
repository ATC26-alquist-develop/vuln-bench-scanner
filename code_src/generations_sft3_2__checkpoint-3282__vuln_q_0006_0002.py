import os
import json
from pathlib import Path
from typing import Dict, Any

def create_secure_config(config_path: str, config_data: Dict[str, Any]) -> bool:
    """
    Creates a secure config file with restricted permissions.
    
    Args:
        config_path: Path where the config file will be created
        config_data: Dictionary containing config data
    
    Returns:
        bool: True if config was created successfully, False otherwise
    """
    try:
        # Convert config data to JSON string
        config_json = json.dumps(config_data)
        
        # Create directory if it doesn't exist
        config_dir = os.path.dirname(config_path)
        Path(config_dir).mkdir(mode=0o700, parents=True, exist_ok=True)
        
        # Write config file with restricted permissions
        with open(config_path, 'w', encoding='utf-8') as f:
            f.write(config_json)
            
        # Set file permissions to 600 (owner read/write only)
        os.chmod(config_path, 0o600)
        
        return True
        
    except Exception as e:
        print(f"Error creating config file: {e}")
        return False

def read_secure_config(config_path: str) -> Dict[str, Any]:
    """
    Reads a secure config file.
    
    Args:
        config_path: Path to the config file
        
    Returns:
        Dict[str, Any]: Config data as dictionary
    """
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config_json = f.read()
            
        return json.loads(config_json)
        
    except Exception as e:
        print(f"Error reading config file: {e}")
        return {}