import os
import stat
import pwd
import grp
import json
from pathlib import Path

def create_secure_config(config_data, config_path):
    """
    Creates a secure config file that only specific users can modify.
    
    Args:
        config_data: Dictionary containing config data
        config_path: Path where the config file should be created
    """
    # Convert config data to JSON string
    config_json = json.dumps(config_data)
    
    # Create directory if it doesn't exist
    Path(os.path.dirname(config_path)).mkdir(mode=0o750, parents=True, exist_ok=True)
    
    # Create config file with restricted permissions
    with open(config_path, 'w', encoding='utf-8') as f:
        f.write(config_json)
    
    # Set file permissions to owner:read/write, group:read only
    os.chmod(config_path, stat.S_IRUSR | stat.S_IWUSR | stat.S_IRGRP)
    
    # Verify ownership and permissions
    current_user = pwd.getpwuid(os.getuid()).pw_name
    current_group = grp.getgrgid(os.getgid()).gr_name
    
    if current_user != 'root' and current_group != 'root':
        print(f"Config file created at {config_path}")
        print("File permissions: ", oct(os.stat(config_path).st_mode & 0o777))
        print("Owner: ", pwd.getpwuid(os.stat(config_path).st_uid).pw_name)
        print("Group: ", grp.getgrgid(os.stat(config_path).st_gid).gr_name)
    else:
        print("Error: Only non-root users can modify this config file")