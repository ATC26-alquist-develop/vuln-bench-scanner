import paramiko
import os
from pathlib import Path
import logging
from typing import Optional

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
        if self.key_path.stat().st_mode & 0o077:  # Check if world-readable
            raise PermissionError("SSH key file has insecure permissions")
            
        # Initialize SSH client
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.RejectPolicy())  # Strict host key checking
        
    def connect(self) -> None:
        """Establish secure SSH connection"""
        try:
            self.client.connect(
                hostname=self.hostname,
                port=self.port,
                username="your_username",  # Set this securely
                key_filename=str(self.key_path),
                timeout=10,  # Set reasonable timeout
                allow_agent=False,
                look_for_keys=False
            )
            self.logger.info("Secure SSH connection established")
        except Exception as e:
            self.logger.error(f"Failed to connect: {str(e)}")
            raise

    def execute_command(self, command: str) -> Optional[str]:
        """Execute command securely"""
        if not isinstance(command, str):
            raise ValueError("Command must be a string")
            
        try:
            with self.client.get_transport() as transport:
                channel = transport.open_channel(
                    "session",
                    destination="stdout",
                    source_address=None
                )
                
            channel.exec_command(command)
            stdout = channel.recv_channel_msg_max_bytes(1024)
            return stdout
        except Exception as e:
            self.logger.error(f"Command execution failed: {str(e)}")
            return None

    def close(self) -> None:
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
        client.connect()
        result = client.execute_command("ls -l")
        print(result)
    except Exception as e:
        logging.error(f"Error: {str(e)}")
    finally:
        client.close()