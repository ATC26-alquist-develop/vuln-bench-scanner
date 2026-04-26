import paramiko
import logging
from typing import Optional
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SecureSSHConnection:
    def __init__(self, hostname: str, username: str, private_key_path: str):
        """Initialize secure SSH connection with proper validation."""
        self.hostname = hostname
        self.username = username
        self.private_key_path = Path(private_key_path)
        
        # Validate inputs
        if not self._validate_hostname(hostname):
            raise ValueError("Invalid hostname format")
        if not self._validate_username(username):
            raise ValueError("Invalid username format")
        if not self._validate_private_key(private_key_path):
            raise ValueError("Invalid private key path")

    def _validate_hostname(self, hostname: str) -> bool:
        """Validate hostname format."""
        return bool(hostname and isinstance(hostname, str) and 
                   hostname.strip() and 
                   len(hostname) <= 255)

    def _validate_username(self, username: str) -> bool:
        """Validate username format."""
        return bool(username and isinstance(username, str) and 
                   username.strip() and 
                   len(username) <= 64)

    def _validate_private_key(self, key_path: str) -> bool:
        """Validate private key file."""
        try:
            key_path = Path(key_path).resolve()
            return key_path.exists() and key_path.is_file() and 
                   key_path.suffix.lower() in ['.pem', '.key']
        except (TypeError, ValueError):
            return False

    def _get_key_filename(self) -> Optional[str]:
        """Get key filename from path."""
        try:
            return str(self.private_key_path.name)
        except (TypeError, ValueError):
            return None

    def connect(self) -> paramiko.SSHClient:
        """Establish secure SSH connection."""
        try:
            # Initialize SSH client
            ssh = paramiko.SSHClient()
            
            # Load system host keys
            ssh.load_system_host_keys()
            
            # Set strict host key policy
            ssh.set_missing_host_key_policy(paramiko.RejectPolicy())
            
            # Attempt to connect
            ssh.connect(
                hostname=self.hostname,
                username=self.username,
                key_filename=self._get_key_filename(),
                timeout=10,
                allow_agent=False,
                look_for_keys=False
            )
            
            logger.info(f"Successfully connected to {self.hostname}")
            return ssh
            
        except paramiko.AuthenticationException:
            logger.error("Authentication failed")
            raise
        except paramiko.SSHException as ssh_exc:
            logger.error(f"SSH error: {str(ssh_exc)}")
            raise
        except Exception as exc:
            logger.error(f"Unexpected error: {str(exc)}")
            raise

# Example usage
if __name__ == "__main__":
    try:
        conn = SecureSSHConnection(
            hostname="example.com",
            username="user",
            private_key_path="/path/to/private_key.pem"
        )
        ssh = conn.connect()
        # Use ssh object for operations
    except Exception as e:
        logger.error(f"Connection failed: {str(e)}")