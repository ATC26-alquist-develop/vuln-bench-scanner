import paramiko
import os
from typing import Optional

def create_ssh_client(
    hostname: str,
    username: str,
    private_key_path: str,
    port: int = 22
) -> Optional[paramiko.SSHClient]:
    """
    Create a secure SSH client with proper key-based authentication.
    
    Args:
        hostname: Target host
        username: SSH username
        private_key_path: Path to the private key file
        port: SSH port (default 22)
    
    Returns:
        SSHClient object or None if authentication fails
    """
    try:
        # Create SSH client
        ssh = paramiko.SSHClient()
        
        # Load system host keys
        ssh.load_system_host_keys()
        
        # Automatically add host keys
        ssh.set_missing_host_key_policy(paramiko.RejectPolicy())
        
        # Load private key
        private_key = paramiko.RSAKey.from_private_key_file(private_key_path)
        
        # Connect with key-based authentication
        ssh.connect(
            hostname=hostname,
            username=username,
            pkey=private_key,
            port=port,
            timeout=10,
            allow_agent=False,
            look_for_keys=False
        )
        
        return ssh
        
    except Exception as e:
        print(f"SSH connection failed: {str(e)}")
        return None

def close_ssh_client(ssh_client: paramiko.SSHClient) -> None:
    """
    Safely close the SSH connection.
    
    Args:
        ssh_client: SSHClient object to close
    """
    if ssh_client:
        ssh_client.close()