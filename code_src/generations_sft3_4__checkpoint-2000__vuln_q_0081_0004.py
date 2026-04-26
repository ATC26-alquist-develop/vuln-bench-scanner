import paramiko
import logging
from typing import Optional
import os
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SecureSSHConnection:
    def __init__(self, hostname: str, username: str, key_path: str):
        """Initialize secure SSH connection with proper validation."""
        if not isinstance(hostname, str) or not hostname:
            raise ValueError("Invalid hostname")
        if not isinstance(username, str) or not username:
            raise ValueError("Invalid username")
        if not isinstance(key_path, str) or not os.path.exists(key_path):
            raise ValueError("Invalid or non-existent key path")

        self.hostname = hostname
        self.username = username
        self.key_path = key_path
        self.client = None

    def connect(self) -> bool:
        """Establish secure SSH connection."""
        try:
            # Create SSH client with secure defaults
            self.client = paramiko.SSHClient()
            self.client.set_missing_host_key_policy(paramiko.RejectPolicy())  # Strict host key checking
            
            # Load private key
            private_key = paramiko.RSAKey.from_private_key_file(self.key_path)
            
            # Attempt connection
            self.client.connect(
                hostname=self.hostname,
                username=self.username,
                pkey=private_key,
                timeout=10,  # Set timeout
                allow_agent=False,
                look_for_keys=False
            )
            logger.info(f"Successfully connected to {self.hostname}")
            return True
            
        except paramiko.AuthenticationException:
            logger.error("Authentication failed")
            return False
        except paramiko.SSHException as ssh_exception:
            logger.error(f"SSH exception occurred: {str(ssh_exception)}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            return False

    def execute_command(self, command: str) -> Optional[str]:
        """Execute command securely."""
        if not isinstance(command, str) or not command.strip():
            logger.error("Invalid command")
            return None

        try:
            stdin, stdout, stderr = self.client.exec_command(command, timeout=30)
            return stdout.read().decode('utf-8')
        except Exception as e:
            logger.error(f"Command execution failed: {str(e)}")
            return None

    def close(self):
        """Safely close the SSH connection."""
        if self.client:
            self.client.close()
            logger.info("SSH connection closed")

def main():
    # Example usage with proper error handling
    try:
        # Validate inputs
        hostname = "example.com"
        username = "user"
        key_path = "/path/to/private_key"
        
        if not all([hostname, username, key_path]):
            raise ValueError("Missing required parameters")
            
        ssh = SecureSSHConnection(hostname, username, key_path)
        if ssh.connect():
            result = ssh.execute_command("ls -l")
            if result:
                print(result)
            ssh.close()
    except Exception as e:
        logger.error(f"Error in main execution: {str(e)}")

if __name__ == "__main__":
    main()