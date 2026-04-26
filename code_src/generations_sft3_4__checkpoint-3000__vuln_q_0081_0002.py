import paramiko
import os
import logging
from typing import Optional
from pathlib import Path

class SecureSSHClient:
    def __init__(self, key_path: str, hostname: str, port: int = 22):
        """
        Initialize secure SSH client with key-based authentication
        
        Args:
            key_path: Path to private key file
            hostname: Target SSH host
            port: SSH port number (default 22)
        """
        # Configure logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        
        # Validate inputs
        if not isinstance(key_path, str) or not isinstance(hostname, str):
            raise ValueError("Invalid input types")
            
        # Validate key file exists and has proper permissions
        key_path = Path(key_path)
        if not key_path.exists():
            raise FileNotFoundError("SSH key file not found")
        if key_path.stat().st_mode & 0o077:  # Check if world-readable
            raise PermissionError("SSH key file has unsafe permissions")
            
        self.hostname = hostname
        self.port = port
        self.key_path = key_path
        
        # Initialize SSH client with secure defaults
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.RejectPolicy())  # Strict host key checking
        
    def connect(self) -> Optional[paramiko.SSHClient]:
        """
        Establish secure SSH connection
        
        Returns:
            SSHClient instance if successful, None if connection fails
        """
        try:
            # Load private key
            private_key = paramiko.RSAKey.from_private_key_file(str(self.key_path))
            
            # Attempt connection
            self.client.connect(
                hostname=self.hostname,
                port=self.port,
                username="your_username",  # Set this securely
                pkey=private_key,
                timeout=10,  # Set reasonable timeout
                allow_agent=False,
                look_for_keys=False
            )
            self.logger.info("Secure SSH connection established")
            return self.client
            
        except paramiko.AuthenticationException:
            self.logger.error("Authentication failed")
            return None
        except paramiko.SSHException as ssh_exc:
            self.logger.error(f"SSH exception: {str(ssh_exc)}")
            return None
        except Exception as e:
            self.logger.error(f"Connection failed: {str(e)}")
            return None

    def __del__(self):
        """Ensure proper cleanup"""
        if hasattr(self, 'client'):
            try:
                self.client.close()
            except Exception:
                pass