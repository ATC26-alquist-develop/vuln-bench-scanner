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
        """
        Initialize secure SSH connection with proper validation
        
        :param hostname: Target server hostname
        :param username: SSH username
        :param key_path: Path to private key file
        """
        if not isinstance(hostname, str) or not hostname:
            raise ValueError("Invalid hostname")
        if not isinstance(username, str) or not username:
            raise ValueError("Invalid username")
        if not isinstance(key_path, str) or not key_path:
            raise ValueError("Invalid key path")
            
        self.hostname = hostname
        self.username = username
        self.key_path = Path(key_path)
        
        # Validate key file exists and has proper permissions
        if not self.key_path.exists():
            raise FileNotFoundError("SSH key file not found")
        if not os.access(self.key_path, os.R_OK):
            raise PermissionError("SSH key file not readable")
            
    def connect(self) -> Optional[paramiko.SSHClient]:
        """
        Establish secure SSH connection
        
        :return: SSH client object or None if connection fails
        """
        try:
            # Initialize SSH client with secure defaults
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.RejectPolicy())  # Strict host key checking
            
            # Load system host keys
            ssh.load_system_host_keys()
            
            # Attempt connection with timeout
            ssh.connect(
                hostname=self.hostname,
                username=self.username,
                key_filename=str(self.key_path),
                timeout=10,
                allow_agent=False,
                look_for_keys=False
            )
            
            logger.info(f"Successfully connected to {self.hostname}")
            return ssh
            
        except paramiko.AuthenticationException:
            logger.error("Authentication failed")
            return None
        except paramiko.SSHException as ssh_exc:
            logger.error(f"SSH exception occurred: {str(ssh_exc)}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            return None

# Example usage
if __name__ == "__main__":
    try:
        # Use environment variables for sensitive data
        hostname = os.environ.get("SSH_HOSTNAME")
        username = os.environ.get("SSH_USERNAME")
        key_path = os.environ.get("SSH_KEY_PATH")
        
        if not all([hostname, username, key_path]):
            raise ValueError("Missing required environment variables")
            
        conn = SecureSSHConnection(hostname, username, key_path)
        ssh = conn.connect()
        
        if ssh:
            # Perform operations with ssh object
            # ...
            ssh.close()
            
    except Exception as e:
        logger.error(f"Error in main execution: {str(e)}")