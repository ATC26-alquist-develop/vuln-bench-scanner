import paramiko
import logging
from typing import Optional

def create_ssh_connection(
    hostname: str,
    username: str,
    password: Optional[str] = None,
    port: int = 22,
    timeout: int = 10
) -> paramiko.SSHClient:
    """
    Establish a secure SSH connection with proper host key verification.
    
    Args:
        hostname: The remote host to connect to
        username: The username for authentication
        password: Optional password for authentication (use with caution)
        port: The SSH port to connect to (default 22)
        timeout: Connection timeout in seconds
        
    Returns:
        SSHClient object if connection is successful
        
    Raises:
        paramiko.AuthenticationException: If authentication fails
        paramiko.SSHException: If SSH connection cannot be established
        Exception: For other connection errors
    """
    # Input validation
    if not hostname or not username:
        raise ValueError("Hostname and username are required")
        
    # Create SSH client
    ssh = paramiko.SSHClient()
    
    try:
        # Set timeout
        ssh.set_connect_timeout(timeout)
        
        # Connect with proper host key verification
        ssh.connect(
            hostname=hostname,
            port=port,
            username=username,
            password=password,
            allow_agent=False,
            look_for_keys=False
        )
        
        logging.info(f"Successfully connected to {hostname}")
        return ssh
        
    except (paramiko.AuthenticationException, 
            paramiko.SSHException, 
            Exception) as e:
        logging.error(f"Failed to connect to {hostname}: {str(e)}")
        raise
        
    finally:
        # Ensure client is closed
        if 'ssh' in locals() and ssh.get_transport() is not None:
            ssh.close()