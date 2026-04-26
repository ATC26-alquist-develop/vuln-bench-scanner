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
        
    def connect(self, hostname: str, username: str, 
                key_path: Optional[str] = None, 
                port: int = 22) -> bool:
        """
        Establishes a secure SSH connection using key-based authentication.
        
        Args:
            hostname: Target server hostname
            username: SSH username
            key_path: Path to private key file
            port: SSH port (default 22)
            
        Returns:
            bool: True if connection successful, False otherwise
        """
        try:
            # Validate inputs
            if not isinstance(hostname, str) or not hostname:
                raise ValueError("Invalid hostname")
            if not isinstance(username, str) or not username:
                raise ValueError("Invalid username")
            if not isinstance(port, int) or port < 1 or port > 65535:
                raise ValueError("Invalid port number")
            
            # Create SSH client
            self.client = paramiko.SSHClient()
            
            # Load system host keys
            self.client.load_system_host_keys()
            # Allow hosts that are signed by the system CA
            self.client.set_missing_host_key_policy(paramiko.RejectPolicy())
            
            # Set timeout
            self.client.connect(
                hostname=hostname,
                username=username,
                key_filename=key_path,
                port=port,
                timeout=10,
                allow_agent=False,
                look_for_keys=False,
                banner_timeout=10,
                auth_timeout=10
            )
            
            logger.info(f"Successfully connected to {hostname}")
            return True
            
        except (paramiko.AuthenticationException, paramiko.SSHException) as e:
            logger.error(f"SSH authentication failed: {str(e)}")
            return False
        except socket.timeout:
            logger.error("Connection timed out")
            return False
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            return False
        finally:
            # Ensure connection is closed
            if self.client:
                try:
                    self.client.close()
                except:
                    pass

    def execute_command(self, command: str) -> Optional[str]:
        """
        Executes a command on the remote server.
        
        Args:
            command: Command to execute
            
        Returns:
            Optional[str]: Command output or None if execution fails
        """
        if not self.client:
            logger.error("No active connection")
            return None
            
        try:
            stdin, stdout, stderr = self.client.exec_command(command)
            return stdout.read().decode('utf-8')
        except Exception as e:
            logger.error(f"Command execution failed: {str(e)}")
            return None
        finally:
            self.client.close()

# Example usage
if __name__ == "__main__":
    ssh = SecureSSHClient()
    if ssh.connect("example.com", "username", "/path/to/private_key"):
        output = ssh.execute_command("ls -l")
        print(output)