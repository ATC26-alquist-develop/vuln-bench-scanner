import os
import json
from pathlib import Path

def create_config_file(config_data, config_path):
    """
    Creates a secure configuration file with the given data.
    
    Args:
        config_data: Dictionary containing configuration data
        config_path: Path where the config file should be created
    """
    # Ensure the path is absolute and normalized
    config_path = Path(config_path).resolve()
    
    # Create parent directories if they don't exist
    config_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Write config data to file
    with open(config_path, 'w', encoding='utf-8') as f:
        json.dump(config_data, f, indent=2)
    
    # Set secure permissions (read/write only for owner)
    os.chmod(config_path, 0o600)

# Example usage
config = {
    "database": {
        "host": "localhost",
        "port": 5432,
        "name": "myapp"
    },
    "logging": {
        "level": "INFO",
        "file": "app.log"
    }
}

create_config_file(config, "/path/to/config.json")