import os
import json
from pathlib import Path
import secrets

def create_secure_config(config_data):
    # Generate a random filename with a secure random token
    filename = f"config_{secrets.token_hex(16)}.json"
    
    # Create a secure path using pathlib
    config_path = Path.home() / "secure_configs" / filename
    
    # Ensure the config directory exists with secure permissions
    config_path.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
    
    # Write config data to file with secure permissions
    try:
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(config_data, f, indent=2)
        os.chmod(config_path, 0o600)  # Only owner can read/write
        return str(config_path)
    except Exception as e:
        print(f"Error creating config file: {e}")
        return None