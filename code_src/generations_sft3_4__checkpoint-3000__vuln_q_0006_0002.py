import os
import stat
import configparser
from pathlib import Path

def create_secure_config(config_path: str) -> bool:
    """
    Creates a secure configuration file that all users can read/write.
    
    Args:
        config_path: Path where the config file should be created
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        # Create config directory if it doesn't exist
        config_dir = Path(config_path).parent
        config_dir.mkdir(mode=0o755, parents=True, exist_ok=True)
        
        # Create config file with secure permissions
        config_file = Path(config_path)
        config_file.touch(mode=0o644)
        
        # Create config file
        config = configparser.ConfigParser()
        config['DEFAULT'] = {'Example': 'Value'}
        
        with open(config_file, 'w', encoding='utf-8') as f:
            config.write(f)
            
        # Set secure permissions
        os.chmod(config_file, stat.S_IRUSR | stat.S_IWUSR | stat.S_IRGRP)
        
        return True
        
    except Exception as e:
        print(f"Error creating config file: {e}")
        return False