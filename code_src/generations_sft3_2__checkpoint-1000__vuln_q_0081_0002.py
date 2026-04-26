import paramiko
import logging
from typing import Optional
from pathlib import Path
import os

class SecureSSHClient:
    def __init__(self, private_key_path: str, timeout: int = 10):
        """
        Initialize secure SSH client with proper error handling and logging.
        
        Args:
            private_key_path: Path to the private key file
            timeout: Connection timeout in seconds
        """
        # Configure logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        
        # Validate private key path
        self.private_key_path = Path(private_key_path)
        if not self.private_key_path.is_file():
            raise ValueError("Private key file does not exist")
            
        # Initialize SSH client with security settings
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.RejectPolicy())  # Strict host key checking
        
        # Set timeout
        self.timeout = timeout
        
    def connect(self, hostname: str, username: str) -> Optional[paramiko.SSHClient]:
        """
        Establish secure SSH connection.
        
        Args:
            hostname: Target hostname
            username: Target username
            
        Returns:
            SSHClient object if connection successful, None otherwise
        """
        try:
            # Validate inputs
            if not hostname or not username:
                raise ValueError("Hostname and username cannot be empty")
                
            # Connect with security settings
            self.client.connect(
                hostname=hostname,
                username=username,
                key_filename=str(self.private_key_path),
                timeout=self.timeout,
                allow_agent=False,
                look_for_keys=False
            )
            self.logger.info(f"Successfully connected to {hostname}")
            return self.client
            
        except paramiko.AuthenticationException:
            self.logger.error("Authentication failed")
            return None
        except paramiko.SSHException as ssh_err:
            self.logger.error(f"SSH error: {str(ssh_err)}")
            return None
        except Exception as e:
            self.logger.error(f"Unexpected error: {str(e)}")
            return None
            
    def close(self):
        """Safely close the SSH connection"""
        if self.client:
            self.client.close()
            self.logger.info("SSH connection closed")