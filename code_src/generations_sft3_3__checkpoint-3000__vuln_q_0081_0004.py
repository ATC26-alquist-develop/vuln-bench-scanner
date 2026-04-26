import paramiko
import socket
import ssl
import logging
from typing import Optional

class SecureSSHConnection:
    def __init__(self):
        # Configure logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        
        # Initialize SSH client with secure defaults
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.RejectPolicy())  # Strict host key checking
        
    def connect(self, hostname: str, username: str, key_path: Optional[str] = None) -> bool:
        """
        Establish a secure SSH connection with proper security controls
        
        Args:
            hostname: Target server hostname
            username: SSH username
            key_path: Optional path to private key file
        
        Returns:
            bool: True if connection successful, False otherwise
        """
        try:
            # Validate inputs
            if not all([hostname, username]):
                self.logger.error("Hostname and username must be provided")
                return False
                
            # Create secure SSL context
            context = ssl.create_default_context()
            context.check_hostname = True
            context.verify_mode = ssl.CERT_REQUIRED
            
            # Connect using secure parameters
            self.client.connect(
                hostname=hostname,
                username=username,
                key_filename=key_path,
                port=22,  # Default SSH port
                ssl_context=context,
                timeout=10,  # Connection timeout
                allow_agent=False,
                look_for_keys=False
            )
            
            self.logger.info(f"Secure connection established to {hostname}")
            return True
            
        except (paramiko.SSHException, socket.error) as e:
            self.logger.error(f"Connection failed: {str(e)}")
            return False
        except Exception as e:
            self.logger.error(f"Unexpected error: {str(e)}")
            return False

    def close(self):
        """Safely close the SSH connection"""
        if self.client:
            self.client.close()
            self.logger.info("SSH connection closed")

# Example usage
if __name__ == "__main__":
    ssh = SecureSSHConnection()
    if ssh.connect("example.com", "username", "/path/to/private_key"):
        # Perform operations here
        ssh.close()