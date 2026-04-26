import paramiko
import socket
import ssl
import logging
from typing import Optional

class SecureSSHConnection:
    def __init__(self, hostname: str, username: str, key_path: str):
        """
        Initialize secure SSH connection with proper validation and security measures.
        
        Args:
            hostname: Target server hostname
            username: SSH username
            key_path: Path to private key file
        """
        # Configure logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        
        # Input validation
        if not isinstance(hostname, str) or not hostname:
            raise ValueError("Invalid hostname")
        if not isinstance(username, str) or not username:
            raise ValueError("Invalid username")
        if not isinstance(key_path, str) or not key_path:
            raise ValueError("Invalid key path")
            
        self.hostname = hostname
        self.username = username
        self.key_path = key_path
        self.client = None

    def connect(self) -> None:
        """
        Establish secure SSH connection using key-based authentication.
        """
        try:
            # Create SSH client with secure defaults
            self.client = paramiko.SSHClient()
            self.client.set_missing_host_key_policy(paramiko.RejectPolicy())  # Strict host key checking
            
            # Load private key
            private_key = paramiko.RSAKey.from_private_key_file(self.key_path)
            
            # Attempt connection with timeout and error handling
            self.client.connect(
                hostname=self.hostname,
                username=self.username,
                pkey=private_key,
                timeout=10,
                allow_agent=False,
                look_for_keys=False,
                banner_timeout=10,
                auth_timeout=10
            )
            
            self.logger.info(f"Successfully connected to {self.hostname}")
            
        except (paramiko.AuthenticationException, paramiko.SSHException) as auth_err:
            self.logger.error(f"Authentication failed: {str(auth_err)}")
            raise
        except socket.timeout:
            self.logger.error("Connection timed out")
            raise
        except Exception as conn_err:
            self.logger.error(f"Connection failed: {str(conn_err)}")
            raise

    def execute_command(self, command: str) -> Optional[str]:
        """
        Execute a command on the remote server securely.
        
        Args:
            command: Command to execute
            
        Returns:
            Command output as string or None if command failed
        """
        if not isinstance(command, str) or not command:
            raise ValueError("Invalid command")
            
        try:
            if not self.client:
                raise RuntimeError("Connection not established")
                
            stdin, stdout, stderr = self.client.exec_command(command)
            return stdout.read().decode('utf-8')
            
        except Exception as cmd_err:
            self.logger.error(f"Command execution failed: {str(cmd_err)}")
            return None

    def close(self) -> None:
        """
        Close the SSH connection.
        """
        if self.client:
            self.client.close()
            self.logger.info("SSH connection closed")

# Example usage
if __name__ == "__main__":
    try:
        # Create connection with proper validation
        ssh = SecureSSHConnection(
            hostname="example.com",
            username="user",
            key_path="/path/to/private_key"
        )
        
        # Establish connection
        ssh.connect()
        
        # Execute command
        output = ssh.execute_command("ls -l")
        if output:
            print(output)
            
        # Close connection
        ssh.close()
        
    except Exception as e:
        print(f"Error: {str(e)}")