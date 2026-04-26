import paramiko
import logging
from typing import Optional
from pathlib import Path

def create_secure_ssh_client(
    hostname: str,
    username: str,
    private_key_path: str,
    timeout: int = 10
) -> Optional[paramiko.SSHClient]:
    """
    Creates a secure SSH client with proper host key verification.
    
    Args:
        hostname: Target hostname
        username: SSH username
        private_key_path: Path to private key file
        timeout: Connection timeout in seconds
    
    Returns:
        SSHClient object or None if connection fails
    """
    try:
        # Configure logging
        logging.basicConfig(level=logging.INFO)
        logger = logging.getLogger(__name__)

        # Initialize SSH client with secure defaults
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.RejectPolicy())  # Reject unknown hosts
        
        # Load private key
        private_key = Path(private_key_path).resolve()
        if not private_key.is_file():
            logger.error("Private key file not found")
            return None
            
        # Attempt to connect with timeout
        ssh.connect(
            hostname=hostname,
            username=username,
            key_filename=str(private_key),
            timeout=timeout,
            allow_agent=False,
            look_for_keys=False
        )
        
        logger.info(f"Successfully connected to {hostname}")
        return ssh
        
    except paramiko.AuthenticationException:
        logger.error("Authentication failed")
        return None
    except paramiko.SSHException as ssh_exc:
        logger.error(f"SSH error: {str(ssh_exc)}")
        return None
    except Exception as exc:
        logger.error(f"Unexpected error: {str(exc)}")
        return None
    finally:
        # Ensure connection is closed
        if 'ssh' in locals() and ssh:
            ssh.close()