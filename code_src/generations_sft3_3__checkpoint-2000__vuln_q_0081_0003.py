import paramiko
import logging
from typing import Optional
from pathlib import Path

def create_secure_ssh_connection(
    hostname: str,
    username: str,
    private_key_path: Path,
    port: int = 22,
    timeout: int = 10
) -> Optional[paramiko.SSHClient]:
    """
    Establishes a secure SSH connection using key-based authentication.
    
    Args:
        hostname: Target hostname
        username: SSH username
        private_key_path: Path to private key file
        port: SSH port (default 22)
        timeout: Connection timeout in seconds
    
    Returns:
        SSHClient object or None if connection fails
    """
    try:
        # Configure logging
        logging.basicConfig(level=logging.INFO)
        logger = logging.getLogger(__name__)

        # Initialize SSH client
        ssh = paramiko.SSHClient()
        
        # Load system host keys
        ssh.load_system_host_keys()
        
        # Strict host key policy
        ssh.set_missing_host_key_policy(paramiko.RejectPolicy())
        
        # Load private key
        private_key = paramiko.RSAKey.from_private_key_file(str(private_key_path))
        
        # Establish connection
        ssh.connect(
            hostname=hostname,
            username=username,
            pkey=private_key,
            port=port,
            timeout=timeout,
            allow_agent=False,
            look_for_keys=False
        )
        
        logger.info(f"Successfully connected to {hostname}")
        return ssh
        
    except paramiko.AuthenticationException:
        logger.error("Authentication failed")
        return None
    except paramiko.SSHException as ssh_ex:
        logger.error(f"SSH exception occurred: {str(ssh_ex)}")
        return None
    except Exception as ex:
        logger.error(f"Unexpected error: {str(ex)}")
        return None
    finally:
        # Ensure connection is closed
        if 'ssh' in locals():
            ssh.close()