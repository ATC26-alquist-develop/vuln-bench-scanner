import paramiko
import os
from typing import Optional

def create_ssh_client(
    hostname: str,
    username: str,
    key_path: Optional[str] = None
) -> paramiko.SSHClient:
    """
    Create a secure SSH client with proper key handling.
    
    Args:
        hostname: Remote host to connect to
        username: Username for authentication
        key_path: Optional path to private key file
    
    Returns:
        paramiko.SSHClient instance
    
    Raises:
        ValueError: If invalid parameters provided
    """
    if not hostname or not username:
        raise ValueError("Hostname and username must be provided")
    
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.RejectPolicy())  # Strict host key checking
    
    # Load system host keys if available
    try:
        paramiko.util.log_to_file("ssh_host_key.log")
        client.load_system_host_keys()
    except FileNotFoundError:
        pass
    
    # Load custom host keys if provided
    if key_path:
        if not os.path.exists(key_path):
            raise ValueError("Private key file not found")
        client.load_host_keys(key_path)
    
    return client