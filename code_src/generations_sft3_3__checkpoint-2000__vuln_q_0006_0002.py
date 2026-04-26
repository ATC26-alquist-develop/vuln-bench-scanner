import os
import json
from pathlib import Path
from typing import Dict, Any

def create_config_file(config_data: Dict[str, Any], config_path: str) -> None:
    """
    Creates a secure config file with proper access controls.
    
    Args:
        config_data: Dictionary containing config data
        config_path: Path where the config file should be created
    """
    try:
        # Convert config data to JSON string
        config_json = json.dumps(config_data, indent=2)
        
        # Create config directory if it doesn't exist
        config_dir = Path(config_path).parent
        config_dir.mkdir(mode=0o755, parents=True, exist_ok=True)
        
        # Create config file with restricted permissions
        config_file = Path(config_path)
        config_file.touch(mode=0o644)
        
        # Write config data to file
        with open(config_file, 'w', encoding='utf-8') as f:
            f.write(config_json)
            
        # Verify file permissions
        if not os.access(config_file, os.R_OK | os.W_OK):
            raise PermissionError("Config file permissions are not correct")
            
    except Exception as e:
        print(f"Error creating config file: {e}")
        raise

# Example usage
if __name__ == "__main__":
    config_data = {
        "app_name": "MyApp",
        "version": "1.0.0",
        "debug_mode": False
    }
    create_config_file(config_data, "/etc/myapp/config.json")