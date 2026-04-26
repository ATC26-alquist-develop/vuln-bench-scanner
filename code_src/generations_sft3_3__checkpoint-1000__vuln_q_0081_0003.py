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
                   len(username) <= 255)

    def _validate_private_key(self, key_path: str) -> bool:
        """Validate private key file."""
        try:
            key_path = Path(key_path).resolve()
            return key_path.exists() and key_path.is_file() and \
                   key_path.suffix.lower() in ['.pem', '.key', '.pkey']
        except (TypeError, ValueError):
            return False

    def _create_ssh_client(self) -> paramiko.SSHClient:
        """Create SSH client with secure defaults."""
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.RejectPolicy())
        return client

    def connect(self) -> Optional[paramiko.SSHClient]:
        """Establish secure SSH connection."""
        try:
            client = self._create_ssh_client()
            
            # Load private key
            key = paramiko.RSAKey.from_private_key_file(str(self.private_key_path))
            
            # Set timeout and disable auto-reconnect
            client.connect(
                hostname=self.hostname,
                username=self.username,
                pkey=key,
                timeout=10,
                allow_agent=False,
                look_for_keys=False,
                banner_timeout=10,
                auth_timeout=10
            )
            
            logger.info(f"Successfully connected to {self.hostname}")
            return client

        except (paramiko.AuthenticationException, paramiko.SSHException) as e:
            logger.error(f"SSH connection failed: {str(e)}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            return None

# Example usage
if __name__ == "__main__":
    try:
        conn = SecureSSHConnection(
            hostname="example.com",
            username="user",
            private_key_path="/path/to/private_key.pem"
        )
        client = conn.connect()
        if client:
            # Use the client for operations...
            client.close()
    except Exception as e:
        logger.error(f"Failed to establish connection: {str(e)}")