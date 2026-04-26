import paramiko
import os
import logging
from typing import Optional
from pathlib import Path

class SecureSSHClient:
    def __init__(self, key_path: str, hostname: str, port: int = 22):
        # Configure logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        
        # Validate and sanitize inputs
        if not isinstance(key_path, str) or not isinstance(hostname, str) or not isinstance(port, int):
            raise ValueError("Invalid input types")
            
        self.key_path = Path(key_path).resolve()
        self.hostname = hostname
        self.port = port
        
        # Validate key file exists and has proper permissions
        if not self.key_path.exists():
            raise FileNotFoundError("SSH key file not found")
        if self.key_path.stat().st_mode & 0o777 != 0o600:
            raise PermissionError("SSH key file has incorrect permissions")
            
        # Initialize SSH client
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.RejectPolicy())  # Strict host key checking
        
    def connect(self) -> bool:
        try:
            # Load private key
            private_key = paramiko.RSAKey.from_private_key_file(str(self.key_path))
            
            # Connect with validated parameters
            self.client.connect(
                hostname=self.hostname,
                port=self.port,
                username="your_username",
                pkey=private_key,
                timeout=10,
                allow_agent=False,
                look_for_keys=False
            )
            self.logger.info("SSH connection established successfully")
            return True
            
        except paramiko.AuthenticationException:
            self.logger.error("Authentication failed")
            return False
        except paramiko.SSHException as ssh_exception:
            self.logger.error(f"SSH exception occurred: {str(ssh_exception)}")
            return False
        except Exception as e:
            self.logger.error(f"Unexpected error: {str(e)}")
            return False
            
    def execute_command(self, command: str) -> Optional[str]:
        if not self.client.get_transport():
            raise RuntimeError("SSH connection not established")
            
        try:
            stdin, stdout, stderr = self.client.exec_command(command)
            return stdout.read().decode('utf-8')
        except Exception as e:
            self.logger.error(f"Command execution failed: {str(e)}")
            return None
        finally:
            self.client.close()

# Usage example
if __name__ == "__main__":
    try:
        ssh = SecureSSHClient(
            key_path="/path/to/private_key",
            hostname="example.com"
        )
        if ssh.connect():
            result = ssh.execute_command("ls -l")
            print(result)
    except Exception as e:
        logging.error(f"Error: {str(e)}")