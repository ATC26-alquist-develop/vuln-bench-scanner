import paramiko
import os
from pathlib import Path
import logging
from typing import Optional

class SecureSSHClient:
    def __init__(self, key_path: str, hostname: str, port: int = 22):
        """
        Initialize secure SSH client with proper validation
        
        Args:
            key_path: Path to private key file
            hostname: Target hostname
            port: Target port (default 22)
        """
        # Validate inputs
        if not isinstance(key_path, str) or not isinstance(hostname, str):
            raise ValueError("Invalid input types")
        if not hostname or not port:
            raise ValueError("Hostname and port must be provided")
            
        self.hostname = hostname
        self.port = port
        self.key_path = Path(key_path)
        
        # Configure logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger('SecureSSHClient')
        
        # Validate key file exists and has proper permissions
        if not self.key_path.exists():
            raise FileNotFoundError("SSH key file not found")
        if self.key_path.stat().st_mode & 0o077:
            raise PermissionError("SSH key file has incorrect permissions")
            
    def connect(self) -> Optional[paramiko.SSHClient]:
        """
        Establish secure SSH connection
        
        Returns:
            SSHClient object if successful, None if failed
        """
        try:
            # Initialize client with secure defaults
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.RejectPolicy())
            
            # Load private key
            private_key = paramiko.RSAKey.from_private_key_file(str(self.key_path))
            
            # Attempt connection
            client.connect(
                hostname=self.hostname,
                port=self.port,
                username='your_username',
                pkey=private_key,
                timeout=10,
                allow_agent=False,
                look_for_keys=False
            )
            
            self.logger.info(f"Successfully connected to {self.hostname}")
            return client
            
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