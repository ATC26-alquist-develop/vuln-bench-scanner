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
        if not key_path.is_file():
            raise FileNotFoundError("SSH key file not found")
            
        # Validate key permissions (should be 600)
        if not os.access(key_path, os.R_OK):
            raise PermissionError("Cannot read SSH key file")
            
        # Create client with secure defaults
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.RejectPolicy())  # Strict host key checking
        
        # Load private key
        try:
            self.client.load_system_host_keys(key_path)
            self.client.connect(
                hostname=hostname,
                port=port,
                username='root',  # Use root only in controlled environments
                key_filename=key_path,
                timeout=10,
                allow_agent=False,
                look_for_keys=False
            )
        except Exception as e:
            self.logger.error(f"SSH connection failed: {str(e)}")
            raise

    def execute_command(self, command: str) -> Optional[str]:
        """
        Execute command securely
        
        Args:
            command: Command to execute
            
        Returns:
            Command output or None on error
        """
        if not isinstance(command, str):
            raise ValueError("Command must be a string")
            
        try:
            stdin, stdout, stderr = self.client.exec_command(
                command,
                timeout=30,
                get_pty=False
            )
            return stdout.read().decode('utf-8')
        except Exception as e:
            self.logger.error(f"Command execution failed: {str(e)}")
            return None

    def close(self):
        """Safely close the SSH connection"""
        self.client.close()

# Example usage
if __name__ == "__main__":
    try:
        # Use environment variables for sensitive data
        key_path = os.environ.get("SSH_KEY_PATH")
        hostname = os.environ.get("SSH_HOSTNAME")
        
        if not key_path or not hostname:
            raise ValueError("Missing required environment variables")
            
        client = SecureSSHClient(key_path, hostname)
        
        # Execute a command
        output = client.execute_command("ls -l")
        print(output)
        
    except Exception as e:
        logging.error(f"Error: {str(e)}")
    finally:
        # Ensure connection is closed
        if 'client' in locals():
            client.close()