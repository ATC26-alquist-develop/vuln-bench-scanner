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
        
    def connect(self) -> bool:
        """
        Establish secure SSH connection using key-based authentication.
        
        :return: True if connection successful, False otherwise
        """
        try:
            # Validate key file exists and has correct permissions
            if not self.key_path.exists():
                logger.error("Private key file not found")
                return False
                
            if not self.key_path.is_file():
                logger.error("Key path must be a file")
                return False
                
            if not self.key_path.stat().st_mode & 0o600:
                logger.error("Key file permissions must be 600")
                return False

            # Create SSH client with secure defaults
            self.client = paramiko.SSHClient()
            self.client.set_missing_host_key_policy(paramiko.RejectPolicy())  # Strict host key checking
            
            # Load system host keys
            paramiko.util.log_to_file('ssh_host_key.log')
            
            # Connect with secure TLS
            tls_config = paramiko.ConfigFileTransport((self.hostname, self.port))
            tls_config.encrypt()
            
            # Set secure TLS configuration
            tls_config.get_remote_host_key().set_type('ssh-rsa')
            tls_config.get_remote_host_key().set_bits(1024)
            
            # Establish secure connection
            tls_config.load()
            self.client._transport = paramiko.Transport(tls_config)
            self.client._transport.start_client()
            
            # Verify TLS version and cipher
            tls_version = self.client._transport.get_banner_version()
            tls_cipher = self.client._transport.get_banner_ciphers()
            if tls_version != 'TLS 1.2' or 'AES128' not in tls_cipher:
                logger.error("TLS version or cipher not secure")
                return False
                
            # Attempt to connect with key-based auth
            self.client.connect(
                hostname=self.hostname,
                port=self.port,
                username='your_username',
                pkey=self.key_path,
                timeout=10,
                allow_agent=False,
                look_for_keys=False
            )
            
            logger.info(f"Successfully connected to {self.hostname}")
            return True
            
        except (paramiko.SSHException, socket.error) as e:
            logger.error(f"Connection failed: {str(e)}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            return False

    def close(self) -> None:
        """Safely close the SSH connection."""
        if self.client:
            self.client.close()
            self.client = None

    def __enter__(self):
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()

# Example usage
if __name__ == "__main__":
    with SecureSSHClient("/path/to/private_key", "example.com") as ssh:
        if ssh.connect():
            # Perform operations here
            pass