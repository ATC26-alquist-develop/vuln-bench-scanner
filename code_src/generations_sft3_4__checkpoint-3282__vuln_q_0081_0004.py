import paramiko
import socket
import logging
from typing import Optional
import ssl

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SecureSSHClient:
    def __init__(self):
        self.client = None
        self._key_file = None
        self._cert_file = None

    def connect(self, hostname: str, port: int = 22, 
                username: str, key_file: Optional[str] = None,
                cert_file: Optional[str] = None) -> bool:
        """
        Establish a secure SSH connection with proper security controls.
        
        Args:
            hostname: Target server hostname
            port: SSH port (default 22)
            username: SSH username
            key_file: Path to private key file
            cert_file: Path to certificate file
        
        Returns:
            bool: True if connection successful, False otherwise
        """
        try:
            # Validate inputs
            if not all([hostname, port, username]):
                logger.error("Missing required parameters")
                return False
                
            # Create SSH client with secure defaults
            self.client = paramiko.SSHClient()
            self.client.set_missing_host_key_policy(paramiko.RejectPolicy())  # Strict host key checking
            
            # Load system host keys
            self.client.load_system_host_keys()
            
            # Configure TLS
            tls_config = paramiko.ConfigParser()
            tls_config['client'] = {
                'cert_reqs': 'CERT_REQUIRED',
                'allow_hostnames': True,
                'hostname': hostname
            }
            self.client._config = tls_config

            # Attempt connection with key authentication
            if key_file:
                self._key_file = key_file
                self.client.connect(
                    hostname=hostname,
                    port=port,
                    username=username,
                    key_filename=key_file,
                    allow_agent=False,
                    look_for_keys=False,
                    timeout=10,
                    banner_timeout=10
                )
            else:
                logger.error("Key file not provided")
                return False

            logger.info(f"Successfully connected to {hostname}")
            return True

        except (paramiko.SSHException, socket.error) as e:
            logger.error(f"Connection failed: {str(e)}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            return False

    def close(self) -> None:
        """Safely close the SSH connection"""
        if self.client:
            self.client.close()
            self.client = None
            logger.info("SSH connection closed")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

# Example usage
if __name__ == "__main__":
    with SecureSSHClient() as ssh:
        if ssh.connect("example.com", 22, "username", "/path/to/private_key"):
            # Perform operations here
            pass