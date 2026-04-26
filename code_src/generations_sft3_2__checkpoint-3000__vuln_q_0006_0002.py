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
        # Convert config data to safe string format
        config_str = configparser.ConfigParser()
        config_str.read_dict(config_data)
        
        # Create directory if it doesn't exist
        config_dir = os.path.dirname(config_path)
        Path(config_dir).mkdir(mode=0o755, parents=True, exist_ok=True)
        
        # Write config file with secure permissions
        with open(config_path, 'w', encoding='utf-8') as config_file:
            config_str.write(config_file)
            
        # Set secure file permissions (owner: r, group: rwx, others: r)
        os.chmod(config_path, stat.S_IRUSR | stat.S_IWUSR | stat.S_IXGRP | stat.S_IRGRP)
        
        return True
        
    except Exception as e:
        print(f"Error creating config file: {e}")
        return False