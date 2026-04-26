import paramiko
import logging
from typing import Optional
import ssl

def create_secure_ssh_connection(
    hostname: str,
    username: str,
    private_key_path: str,
    port: int = 22,
    timeout: int = 10
) -> Optional[paramiko.SSHClient]:
    """
    Creates a secure SSH connection using key-based authentication only.
    
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

        # Initialize SSH client with secure defaults
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.RejectPolicy())  # Explicit policy
        
        # Load private key
        private_key = paramiko.RSAKey.from_private_key_file(private_key_path)
        
        # Establish connection with security controls
        ssh.connect(
            hostname=hostname,
            username=username,
            pkey=private_key,
            port=port,
            timeout=timeout,
            allow_agent=False,
            look_for_keys=False,
            banner_timeout=timeout,
            auth_timeout=timeout
        )
        
        logger.info(f"Secure SSH connection established to {hostname}")
        return ssh
        
    except paramiko.AuthenticationException:
        logger.error("Authentication failed")
        return None
    except paramiko.SSHException as ssh_ex:
        logger.error(f"Lower level SSH exception: {str(ssh_ex)}")
        return None
    except ssl.SSLError as ssl_ex:
        logger.error(f"SSL error: {str(ssl_ex)}")
        return None
    except Exception as ex:
        logger.error(f"Unexpected error: {str(ex)}")
        return None
    finally:
        # Ensure connection is closed
        if 'ssh' in locals():
            try:
                ssh.close()
            except Exception:
                pass