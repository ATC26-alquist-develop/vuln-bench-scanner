import paramiko
import socket
import ssl
from typing import Optional
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SecureSSHClient:
    def __init__(self, key_path: str, hostname: str, port: int = 22):
        """
        Initialize secure SSH client with key-based authentication.
        
        :param key_path: Path to private key file
        :param hostname: Target hostname
        :param port: SSH port (default 22)
        """
        self.key_path = Path(key_path)
        self.hostname = hostname
        self.port = port
        self.client = None
        
        # Validate key file
        if not self.key_path.exists():
            raise FileNotFoundError(f"SSH key file not found: {key_path}")
        
        # Verify key permissions
        if not self.key_path.is_file():
            raise ValueError("Key path must point to a file")
        if not self.key_path.stat().st_mode & 0o777:
            raise PermissionError("Key file permissions too permissive")

    def connect(self) -> None:
        """Establish secure SSH connection"""
        try:
            # Create SSH client
            self.client = paramiko.SSHClient()
            
            # Load system host keys
            self.client.load_system_host_keys()
            
            # Strict host key policy
            self.client.set_missing_host_key_policy(paramiko.RejectPolicy())
            
            # Connect with timeout
            self.client.connect(
                hostname=self.hostname,
                port=self.port,
                username="your_username",
                pkey=self._get_key(),
                timeout=10,
                allow_agent=False,
                look_for_keys=False
            )
            
            logger.info(f"Successfully connected to {self.hostname}")
            
        except (paramiko.SSHException, socket.error) as e:
            logger.error(f"SSH connection failed: {str(e)}")
            raise

    def _get_key(self) -> paramiko.PKey:
        """Securely load private key"""
        try:
            key = paramiko.RSAKey.from_private_key_file(str(self.key_path))
            return key
        except paramiko.SSHException as e:
            logger.error(f"Key loading failed: {str(e)}")
            raise

    def execute_command(self, command: str) -> Optional[str]:
        """Execute command securely"""
        if not self.client:
            raise ConnectionError("Not connected to SSH server")
            
        try:
            stdin, stdout, stderr = self.client.exec_command(command, timeout=30)
            return stdout.read().decode('utf-8')
        except (socket.timeout, paramiko.SSHException) as e:
            logger.error(f"Command execution failed: {str(e)}")
            return None

    def close(self) -> None:
        """Safely close the connection"""
        if self.client:
            self.client.close()
            logger.info("SSH connection closed")

# Example usage
if __name__ == "__main__":
    try:
        client = SecureSSHClient("/path/to/private_key", "example.com")
        client.connect()
        
        # Execute a command
        output = client.execute_command("ls -l")
        if output:
            print(output)
        
        client.close()
    except Exception as e:
        logger.error(f"Error: {str(e)}")