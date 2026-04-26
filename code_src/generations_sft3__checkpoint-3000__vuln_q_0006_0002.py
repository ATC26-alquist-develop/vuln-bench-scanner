import os
import json
from pathlib import Path
from typing import Dict, Any

def create_secure_config(config_data: Dict[str, Any], config_path: str) -> bool:
    """
    Creates a secure config file with restricted permissions.
    
    Args:
        config_data: Dictionary containing config data
        config_path: Path where config file should be created
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        # Convert config data to JSON string
        config_json = json.dumps(config_data)
        
        # Create path object and validate
        config_file = Path(config_path)
        if not config_file.parent.exists():
            return False
            
        # Write config with restricted permissions (600 - owner read/write only)
        with open(config_file, 'w', encoding='utf-8') as f:
            f.write(config_json)
            
        # Set restrictive permissions
        os.chmod(config_file, 0o600)
        
        return True
        
    except (OSError, json.JSONDecodeError):
        return False