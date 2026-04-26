import paramiko
import logging
from typing import Optional
from pathlib import Path
import os

class SecureSSHClient:
    def __init__(self, config_path: str):
        """Initialize SSH client with proper security controls."""
        # Validate config path
        self.config_path = Path(config_path).resolve()
        if not self.config_path.exists():
            raise ValueError("SSH configuration file does not exist")
            
        # Configure logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        
        # Initialize SSH client with security settings
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.RejectPolicy())
        
    def connect(self, username: str, hostname: str, port: int = 22) -> bool:
        """Establish secure SSH connection."""
        try:
            # Validate inputs
            if not all([username, hostname, port]):
                raise ValueError("Missing required parameters")
                
            # Load private key
            private_key_path = self.config_path / "id_rsa"
            if not private_key_path.exists():
                raise ValueError("Private key file not found")
                
            # Load private key with security controls
            private_key = paramiko.RSAKey.from_private_key_file(str(private_key_path))
            
            # Establish connection
            self.client.connect(
                hostname=hostname,
                port=port,
                username=username,
                pkey=private_key,
                timeout=10,
                allow_agent=False,
                look_for_keys=False
            )
            
            self.logger.info(f"Successfully connected to {hostname}")
            return True
            
        except Exception as e:
            self.logger.error(f"Connection failed: {str(e)}")
            return False
            
    def execute_command(self, command: str) -> Optional[str]:
        """Execute a command securely."""
        try:
            if not self.client:
                raise ValueError("SSH connection not established")
                
            stdin, stdout, stderr = self.client.exec_command(command)
            return stdout.read().decode()
            
        except Exception as e:
            self.logger.error(f"Command execution failed: {str(e)}")
            return None
            
    def close(self):
        """Safely close the SSH connection."""
        if self.client:
            self.client.close()
            self.logger.info("SSH connection closed")

# Example usage
if __name__ == "__main__":
    try:
        ssh = SecureSSHClient("/path/to/config")
        if ssh.connect(username="user", hostname="example.com"):
            result = ssh.execute_command("ls -l")
            print(result)
            ssh.close()
    except Exception as e:
        print(f"Error: {str(e)}")