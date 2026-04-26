import paramiko
import os
import logging
from typing import Optional
from pathlib import Path

class SecureSSHClient:
    def __init__(self, key_path: str, hostname: str, port: int = 22):
        # Configure logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        
        # Validate inputs
        if not isinstance(key_path, str) or not isinstance(hostname, str) or not isinstance(port, int):
            raise ValueError("Invalid input types")
            
        self.hostname = hostname
        self.port = port
        
        # Validate key file exists and has proper permissions
        key_path = Path(key_path)
        if not key_path.is_file():
            raise FileNotFoundError("SSH key file not found")
        if key_path.stat().st_mode & 0o077:  # Check if world-readable/writable
            raise PermissionError("SSH key file has unsafe permissions")
            
        # Create client with secure defaults
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.RejectPolicy())  # Strict host key checking
        
    def connect(self) -> None:
        """Establish secure SSH connection"""
        try:
            # Load private key with password
            private_key = paramiko.RSAKey.from_private_key_file(str(key_path))
            self.client.connect(
                hostname=self.hostname,
                port=self.port,
                username="your_username",
                pkey=private_key,
                timeout=10,
                allow_agent=False,
                look_for_keys=False
            )
            self.logger.info("Secure SSH connection established")
        except Exception as e:
            self.logger.error(f"Failed to connect: {str(e)}")
            raise

    def execute_command(self, command: str) -> Optional[str]:
        """Execute command securely"""
        if not command or not isinstance(command, str):
            raise ValueError("Invalid command")
            
        try:
            with self.client.get_transport() as transport:
                channel = transport.open_channel(
                    'session',
                    destination=command,
                    source_address=None
                )
                
            channel.exec_command(command)
            output = channel.recv(65535)
            return output.decode('utf-8')
        except Exception as e:
            self.logger.error(f"Command execution failed: {str(e)}")
            return None

    def close(self) -> None:
        """Safely close the SSH connection"""
        if self.client:
            self.client.close()
            self.logger.info("SSH connection closed")