import paramiko
import socket
import logging
from typing import Optional
import ssl

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SecureSSHClient:
    def __init__(self):
        self.client = None
        self._key_file = None
        self._cert_file = None

    def connect(self, hostname: str, port: int = 22, 
                username: str, key_file: Optional[str] = None,
                cert_file: Optional[str] = None) -> bool:
        """
        Establish a secure SSH connection with proper security controls.
        
        Args:
            hostname: Target server hostname
            port: SSH port (default 22)
            username: SSH username
            key_file: Path to private key file
            cert_file: Path to certificate file
        
        Returns:
            bool: True if connection successful, False otherwise
        """
        try:
            # Validate inputs
            if not all([hostname, port, username]):
                logger.error("Missing required connection parameters")
                return False
                
            # Create SSH client with secure defaults
            self.client = paramiko.SSHClient()
            self.client.set_missing_host_key_policy(paramiko.RejectPolicy())  # Strict host key checking
            
            # Load system host keys
            self.client.load_system_host_keys()
            
            # Set timeout
            self.client.connect(
                hostname=hostname,
                port=port,
                username=username,
                key_filename=key_file,
                cert_filename=cert_file,
                timeout=10,
                allow_agent=False,
                look_for_keys=False,
                banner_timeout=10,
                gss_auth=False,
                gss_kex=False
            )
            
            logger.info(f"Successfully connected to {hostname}")
            return True
            
        except socket.timeout:
            logger.error("Connection timed out")
            return False
        except paramiko.AuthenticationException:
            logger.error("Authentication failed")
            return False
        except paramiko.SSHException as ssh_exc:
            logger.error(f"SSH exception occurred: {ssh_exc}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            return False
        finally:
            # Ensure connection is closed
            if self.client:
                try:
                    self.client.close()
                except Exception:
                    pass

    def __del__(self):
        """Ensure proper cleanup of resources"""
        if self.client:
            try:
                self.client.close()
            except Exception:
                pass