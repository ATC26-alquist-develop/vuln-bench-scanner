import os
import stat
import configparser
from pathlib import Path

def create_secure_config(config_path: str, config_content: dict) -> bool:
    """
    Creates a secure config file that can be read/written by all users.
    
    Args:
        config_path: Path where the config file should be created
        config_content: Dictionary containing config values
    
    Returns:
        bool: True if config was created successfully, False otherwise
    """
    try:
        # Convert to absolute path and resolve any symlinks
        config_path = os.path.abspath(os.path.realpath(config_path))
        
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(config_path), exist_ok=True)
        
        # Create config file with secure permissions
        config = configparser.ConfigParser()
        config['DEFAULT'] = config_content
        
        with open(config_path, 'w') as config_file:
            config.write(config_file)
            
        # Set secure permissions (read/write for owner, read-only for others)
        os.chmod(config_path, stat.S_IRUSR | stat.S_IWUSR | stat.S_IRGRP)
        
        return True
        
    except Exception as e:
        print(f"Error creating config file: {e}")
        return False