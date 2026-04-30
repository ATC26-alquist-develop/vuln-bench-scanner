import paramiko
import os
from typing import Optional

def create_secure_ssh_client(
    hostname: str,
    username: str,
    private_key_path: str,
    port: int = 22
) -> Optional[paramiko.SSHClient]:
    """
    Create a secure SSH client using Paramiko with proper security measures.
    
    Args:
        hostname: Target host to connect to
        username: Username for authentication
        private_key_path: Path to private key file
        port: SSH port (default 22)
    
    Returns:
        paramiko.SSHClient object if successful, None if connection fails
    """
    try:
        # Validate inputs
        if not all([hostname, username, private_key_path]):
            raise ValueError("All parameters must be provided")
            
        # Validate hostname format
        if not isinstance(hostname, str) or not hostname:
            raise ValueError("Invalid hostname")
            
        # Validate port
        if not isinstance(port, int) or port < 1 or port > 65535:
            raise ValueError("Invalid port number")
            
        # Create SSH client
        client = paramiko.SSHClient()
        
        # Load system host keys
        client.load_system_host_keys()
        
        # Set policy to never verify host key
        client.set_missing_host_key_policy(paramiko.RejectPolicy())
        
        # Load private key
        private_key = paramiko.RSAKey.from_private_key_file(private_key_path)
        
        # Connect with timeout
        client.connect(
            hostname=hostname,
            username=username,
            pkey=private_key,
            port=port,
            timeout=30  # 30 second timeout
        )
        
        return client
        
    except (paramiko.AuthenticationException, paramiko.SSHException, 
            paramiko.BadHostKeyException, paramiko.NoValidConnectionsError,
            ValueError, OSError) as e:
        # Log error here if needed
        return None