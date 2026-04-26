import paramiko
import socket
import ssl
from typing import Optional
import logging
from pathlib import Path

class SecureSSHClient:
    def __init__(self, key_path: str, hostname: str, port: int = 22):
        """
        Initialize secure SSH client with key-based authentication.
        
        :param key_path: Path to private key file
        :param hostname: Target hostname
        :param port: SSH port (default 22)
        """
        # Configure logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        
        # Validate inputs
        if not isinstance(key_path, str) or not isinstance(hostname, str):
            raise ValueError("Invalid input types")
        if not hostname:
            raise ValueError("Hostname cannot be empty")
            
        self.key_path = Path(key_path)
        self.hostname = hostname
        self.port = port
        
        # Verify key file exists and has proper permissions
        if not self.key_path.is_file():
            raise FileNotFoundError("SSH key file not found")
        if self.key_path.stat().st_mode & 0o077:
            raise PermissionError("SSH key file has incorrect permissions")
            
        # Initialize SSH client
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.RejectPolicy())  # Strict host key checking
        
    def connect(self) -> Optional[paramiko.SSHClient]:
        """
        Establish secure SSH connection.
        
        :return: SSH client object if connection successful, None otherwise
        """
        try:
            # Load private key
            private_key = paramiko.RSAKey.from_private_key_file(str(self.key_path))
            
            # Create secure SSL context
            ssl_context = ssl.create_default_context()
            ssl_context.check_hostname = True
            ssl_context.verify_mode = ssl.CERT_REQUIRED
            
            # Connect using secure SSH
            self.client.connect(
                hostname=self.hostname,
                port=self.port,
                username="your_username",
                pkey=private_key,
                timeout=10,
                ssl_context=ssl_context,
                allow_agent=False,
                look_for_keys=False
            )
            
            self.logger.info(f"Successfully connected to {self.hostname}")
            return self.client
            
        except (paramiko.AuthenticationException, paramiko.SSHException) as e:
            self.logger.error(f"SSH connection failed: {str(e)}")
            return None
        except socket.error as e:
            self.logger.error(f"Socket error: {str(e)}")
            return None
        except Exception as e:
            self.logger.error(f"Unexpected error: {str(e)}")
            return None

    def __del__(self):
        """Ensure proper cleanup of resources"""
        if hasattr(self, 'client'):
            self.client.close()