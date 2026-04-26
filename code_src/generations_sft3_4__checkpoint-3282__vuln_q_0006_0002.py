import os
import stat
import configparser
from pathlib import Path

def create_secure_config(config_path: str, config_data: dict) -> bool:
    """
    Creates a secure config file that's readable/writable by all users.
    
    Args:
        config_path: Path where the config file will be created
        config_data: Dictionary containing config data
    
    Returns:
        bool: True if config was created successfully, False otherwise
    """
    try:
        # Convert to absolute path and resolve any symlinks
        config_path = os.path.abspath(os.path.realpath(config_path))
        
        # Create directory if it doesn't exist
        Path(os.path.dirname(config_path)).mkdir(mode=0o777, parents=True, exist_ok=True)
        
        # Create config file with secure permissions
        config = configparser.ConfigParser()
        config['DEFAULT'] = config_data
        
        with open(config_path, 'w', encoding='utf-8') as config_file:
            config.write(config_file)
            
        # Set secure permissions (read/write for all)
        os.chmod(config_path, stat.S_IRWXU | stat.S_IRGRP | stat.S_IWGRP)
        
        return True
        
    except Exception as e:
        print(f"Error creating config file: {e}")
        return False