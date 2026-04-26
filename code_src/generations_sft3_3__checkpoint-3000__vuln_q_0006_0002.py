import os
import configparser
import stat
from pathlib import Path

def create_secure_config(config_path: str, config_data: dict) -> bool:
    """
    Creates a secure config file with proper permissions.
    
    Args:
        config_path: Path where the config file should be created
        config_data: Dictionary containing config data
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        # Convert config data to a safe format
        config = configparser.ConfigParser()
        config.read_dict(config_data)
        
        # Create directory if it doesn't exist
        config_dir = Path(config_path).parent
        config_dir.mkdir(mode=0o755, parents=True, exist_ok=True)
        
        # Create config file with secure permissions
        config_file = Path(config_path)
        config_file.touch(mode=0o644)
        
        # Write config to file
        with open(config_file, 'w', encoding='utf-8') as f:
            config.write(f)
            
        # Set secure permissions
        os.chmod(config_file, stat.S_IRUSR | stat.S_IWUSR | stat.S_IRGRP)
        
        return True
        
    except Exception as e:
        print(f"Error creating config file: {e}")
        return False