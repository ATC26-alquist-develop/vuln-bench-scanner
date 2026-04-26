import paramiko
import logging
from typing import Optional
import ssl
import os
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SecureSSHClient:
    def __init__(self, hostname: str, username: str, key_path: str):
        """Initialize SSH client with secure defaults."""
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
        if not self.key_path.exists():
            raise FileNotFoundError("SSH key file not found")
        if not os.access(self.key_path, os.R_OK):
            raise PermissionError("SSH key file not readable")
            
        # Create SSH client with secure defaults
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.RejectPolicy())  # Strict host key checking
        
    def connect(self) -> Optional[paramiko.SSHClient]:
        """Establish secure SSH connection."""
        try:
            # Load key
            private_key = paramiko.RSAKey.from_private_key_file(str(self.key_path))
            
            # Set timeout and disable auto-reconnect
            self.client.connect(
                hostname=self.hostname,
                username=self.username,
                pkey=private_key,
                timeout=10,
                allow_agent=False,
                look_for_keys=False,
                banner_timeout=10,
                auth_timeout=10
            )
            logger.info(f"Successfully connected to {self.hostname}")
            return self.client
            
        except paramiko.AuthenticationException:
            logger.error("Authentication failed")
            return None
        except paramiko.SSHException as ssh_ex:
            logger.error(f"SSH exception occurred: {str(ssh_ex)}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            return None

    def close(self):
        """Safely close the SSH connection."""
        if self.client:
            self.client.close()
            logger.info("SSH connection closed")

def main():
    # Example usage with secure defaults
    try:
        hostname = "example.com"
        username = "user"
        key_path = "/path/to/private_key"
        
        client = SecureSSHClient(hostname, username, key_path)
        ssh_connection = client.connect()
        
        if ssh_connection:
            # Perform operations here
            logger.info("Performing operations...")
            client.close()
            
    except Exception as e:
        logger.error(f"Error in main: {str(e)}")

if __name__ == "__main__":
    main()