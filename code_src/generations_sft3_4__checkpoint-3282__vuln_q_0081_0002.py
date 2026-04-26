import paramiko
import os
import logging
from typing import Optional
from pathlib import Path

class SecureSSHClient:
    def __init__(self, key_path: str, hostname: str, port: int = 22):
        # Validate inputs
        if not isinstance(key_path, str) or not isinstance(hostname, str) or not isinstance(port, int):
            raise ValueError("Invalid input types")
        
        self.hostname = hostname
        self.port = port
        self.key_path = Path(key_path)
        
        # Configure logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        
        # Validate key file exists and has proper permissions
        if not self.key_path.exists():
            raise FileNotFoundError("SSH key file not found")
        if self.key_path.stat().st_mode & 0o077:  # Check if world-readable/writable
            raise PermissionError("SSH key file has insecure permissions")
            
        # Initialize SSH client
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.RejectPolicy())  # Strict host key checking
        
    def connect(self) -> Optional[paramiko.SSHClient]:
        """Establish secure SSH connection"""
        try:
            self.client.connect(
                hostname=self.hostname,
                port=self.port,
                username=os.environ.get('SSH_USERNAME'),
                key_filename=str(self.key_path),
                timeout=10,
                allow_agent=False,
                look_for_keys=False
            )
            self.logger.info(f"Successfully connected to {self.hostname}")
            return self.client
            
        except paramiko.AuthenticationException:
            self.logger.error("Authentication failed")
            return None
        except paramiko.SSHException as ssh_err:
            self.logger.error(f"SSH exception occurred: {ssh_err}")
            return None
        except Exception as e:
            self.logger.error(f"Connection failed: {str(e)}")
            return None

    def close(self):
        """Safely close the SSH connection"""
        if self.client:
            self.client.close()
            self.logger.info("SSH connection closed")

# Usage example
if __name__ == "__main__":
    try:
        client = SecureSSHClient(
            key_path="/path/to/private_key",
            hostname="example.com"
        )
        conn = client.connect()
        if conn:
            # Perform operations here
            pass
    except Exception as e:
        logging.error(f"Failed to initialize SSH client: {str(e)}")