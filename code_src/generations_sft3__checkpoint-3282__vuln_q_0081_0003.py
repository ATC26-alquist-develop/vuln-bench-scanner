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
    Establishes a secure SSH connection using key-based authentication only.
    
    Args:
        hostname: Target host to connect to
        username: SSH username
        private_key_path: Path to private key file
        port: SSH port (default 22)
        timeout: Connection timeout in seconds
    
    Returns:
        SSHClient object if connection successful, None otherwise
    """
    # Configure logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    try:
        # Initialize SSH client with secure defaults
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.RejectPolicy())  # Explicit policy
        
        # Load private key
        try:
            private_key = paramiko.RSAKey.from_private_key_file(str(private_key_path))
        except Exception as e:
            logger.error(f"Failed to load private key: {e}")
            return None

        # Add host key explicitly
        ssh.get_host_keys().add(hostname, 'ssh-rsa', private_key)

        # Attempt connection with timeout
        ssh.connect(
            hostname=hostname,
            username=username,
            pkey=private_key,
            port=port,
            timeout=timeout,
            allow_agent=False,
            look_for_keys=False,
            banner_timeout=timeout
        )
        logger.info(f"Successfully connected to {hostname}")
        return ssh

    except paramiko.AuthenticationException:
        logger.error("Authentication failed")
        return None
    except paramiko.SSHException as ssh_exception:
        logger.error(f"SSH exception occurred: {ssh_exception}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return None
    finally:
        # Ensure connection is closed
        if ssh:
            try:
                ssh.close()
            except Exception:
                pass