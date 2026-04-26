import os
import json
from pathlib import Path
from typing import Dict, Any

def create_config_file(config_data: Dict[str, Any], config_path: str) -> bool:
    """
    Creates a secure config file with proper access controls.
    
    Args:
        config_data: Dictionary containing config data
        config_path: Path where config file should be created
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        # Convert config data to JSON string
        config_json = json.dumps(config_data, indent=2)
        
        # Create config directory if it doesn't exist
        config_dir = Path(config_path).parent
        config_dir.mkdir(mode=0o750, parents=True, exist_ok=True)
        
        # Create config file with restricted permissions
        config_file = Path(config_path)
        config_file.touch(mode=0o640)
        
        # Write config data to file
        with open(config_file, 'w', encoding='utf-8') as f:
            f.write(config_json)
            
        return True
        
    except (OSError, json.JSONDecodeError) as e:
        print(f"Error creating config file: {e}")
        return False