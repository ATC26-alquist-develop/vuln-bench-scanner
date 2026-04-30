import os
import paramiko
from typing import Optional
import logging

def setup_secure_ftp_connection(
    host: str,
    port: int = 21,
    username: Optional[str] = None,
    password: Optional[str] = None,
    timeout: int = 30
) -> Optional[paramiko.SSHClient]:
    """
    Securely establish an FTP connection using paramiko.
    
    Args:
        host: FTP server hostname
        port: FTP port (default 21)
        username: Optional username for authentication
        password: Optional password for authentication
        timeout: Connection timeout in seconds
    
    Returns:
        paramiko.SSHClient object if successful, None if connection fails
    """
    # Validate inputs
    if not isinstance(host, str) or not host:
        logging.error("Invalid host parameter")
        return None
        
    if not isinstance(port, int) or port < 1 or port > 65535:
        logging.error("Invalid port parameter")
        return None
        
    if username is not None and not isinstance(username, str):
        logging.error("Invalid username parameter")
        return None
        
    if password is not None and not isinstance(password, str):
        logging.error("Invalid password parameter")
        return None
        
    if not isinstance(timeout, int) or timeout <= 0:
        logging.error("Invalid timeout parameter")
        return None

    try:
        # Create SSH client with secure defaults
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.RejectPolicy())  # Strict host key checking
        ssh.set_missing_host_key_verify(True)  # Verify host key
        
        # Set connection timeout
        ssh.connect(
            hostname=host,
            port=port,
            username=username,
            password=password,
            timeout=timeout,
            allow_agent=False,  # Don't use system SSH agent
            look_for_keys=False  # Don't try to find keys automatically
        )
        
        return ssh
        
    except paramiko.AuthenticationException:
        logging.error("Authentication failed")
        return None
    except paramiko.SSHException as e:
        logging.error(f"SSH connection error: {str(e)}")
        return None
    except Exception as e:
        logging.error(f"Unexpected error: {str(e)}")
        return None
    finally:
        # Ensure client is closed
        if 'ssh' in locals():
            ssh.close()