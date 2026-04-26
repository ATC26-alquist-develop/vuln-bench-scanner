import paramiko
import os
import logging
from typing import Optional
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SecureSSHConnection:
    def __init__(self, hostname: str, username: str, key_path: str):
        """
        Initialize secure SSH connection with proper validation and error handling.
        
        :param hostname: Target server hostname
        :param username: SSH username
        :param key_path: Path to private key file
        """
        self.hostname = hostname
        self.username = username
        self.key_path = Path(key_path)
        
        # Validate inputs
        if not self._validate_hostname(hostname):
            raise ValueError("Invalid hostname format")
        if not self._validate_username(username):
            raise ValueError("Invalid username format")
        if not self._validate_key_path(key_path):
            raise ValueError("Invalid key path")

    def _validate_hostname(self, hostname: str) -> bool:
        """Validate hostname format."""
        return bool(hostname and hostname.strip())

    def _validate_username(self, username: str) -> bool:
        """Validate username format."""
        return bool(username and username.strip())

    def _validate_key_path(self, key_path: str) -> bool:
        """Validate key path."""
        return bool(key_path and Path(key_path).is_file())

    def _get_key_path(self) -> Optional[Path]:
        """Safely get key path."""
        try:
            return Path(self.key_path).resolve()
        except (TypeError, ValueError):
            logger.error("Invalid key path")
            return None

    def connect(self) -> Optional[paramiko.SSHClient]:
        """
        Establish secure SSH connection.
        
        :return: SSH client object or None if connection fails
        """
        try:
            # Initialize SSH client
            ssh = paramiko.SSHClient()
            
            # Load system host keys
            ssh.load_system_host_keys()
            
            # Set strict host key policy
            ssh.set_missing_host_key_policy(paramiko.RejectPolicy())
            
            # Load private key
            key_path = self._get_key_path()
            if not key_path:
                return None
                
            # Connect using private key
            ssh.connect(
                hostname=self.hostname,
                username=self.username,
                key_filename=str(key_path),
                timeout=10,
                allow_agent=False,
                look_for_keys=False
            )
            
            logger.info(f"Successfully connected to {self.hostname}")
            return ssh
            
        except paramiko.AuthenticationException:
            logger.error("Authentication failed")
        except paramiko.SSHException as ssh_exc:
            logger.error(f"SSH exception: {str(ssh_exc)}")
        except Exception as exc:
            logger.error(f"Unexpected error: {str(exc)}")
            
        return None

# Example usage
if __name__ == "__main__":
    try:
        conn = SecureSSHConnection(
            hostname="example.com",
            username="user",
            key_path="/path/to/private_key"
        )
        ssh = conn.connect()
        if ssh:
            # Use ssh object for operations
            pass
    except Exception as e:
        logger.error(f"Failed to establish connection: {str(e)}")