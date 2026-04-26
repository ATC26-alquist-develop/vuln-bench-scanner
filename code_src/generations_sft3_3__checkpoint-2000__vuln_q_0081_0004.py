import paramiko
import logging
from typing import Optional
import os
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SecureSSHConnection:
    def __init__(self, hostname: str, username: str, key_path: str):
        """Initialize secure SSH connection with proper validation."""
        if not isinstance(hostname, str) or not hostname:
            raise ValueError("Invalid hostname")
        if not isinstance(username, str) or not username:
            raise ValueError("Invalid username")
        if not isinstance(key_path, str) or not key_path:
            raise ValueError("Invalid key path")
            
        self.hostname = hostname
        self.username = username
        self.key_path = Path(key_path)
        
        # Validate key file exists and has proper permissions
        if not self.key_path.is_file():
            raise FileNotFoundError("SSH key file not found")
        if not os.access(self.key_path, os.R_OK):
            raise PermissionError("SSH key file not readable")
            
        # Configure SSH client with security settings
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.RejectPolicy())  # Strict host key checking
        
    def connect(self) -> Optional[paramiko.SSHClient]:
        """Establish secure SSH connection."""
        try:
            # Load private key
            private_key = paramiko.RSAKey.from_private_key_file(str(self.key_path))
            
            # Attempt connection with strict security settings
            self.client.connect(
                hostname=self.hostname,
                username=self.username,
                pkey=private_key,
                timeout=10,
                allow_agent=False,
                look_for_keys=False,
                banner_timeout=10,
                gss_auth=False,
                auth_timeout=10
            )
            logger.info(f"Successfully connected to {self.hostname}")
            return self.client
            
        except paramiko.AuthenticationException:
            logger.error("Authentication failed")
            raise
        except paramiko.SSHException as ssh_exception:
            logger.error(f"SSH exception occurred: {str(ssh_exception)}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            raise

    def close(self):
        """Safely close the SSH connection."""
        if self.client:
            self.client.close()
            logger.info("SSH connection closed")

# Example usage
if __name__ == "__main__":
    try:
        # Use environment variables for sensitive data
        hostname = os.environ.get("SSH_HOSTNAME")
        username = os.environ.get("SSH_USERNAME")
        key_path = os.environ.get("SSH_KEY_PATH")
        
        if not all([hostname, username, key_path]):
            raise ValueError("Missing required environment variables")
            
        connection = SecureSSHConnection(hostname, username, key_path)
        client = connection.connect()
        
        if client:
            # Perform operations here
            client.close()
            
    except Exception as e:
        logger.error(f"Error in main execution: {str(e)}")