import paramiko
import os
from typing import Optional

def create_ssh_connection(
    hostname: str,
    username: str,
    private_key_path: str,
    port: int = 22
) -> Optional[paramiko.SSHClient]:
    """
    Establish a secure SSH connection using paramiko.
    
    Args:
        hostname: Remote server hostname
        username: Username for SSH connection
        private_key_path: Path to private key file
        port: SSH port (default: 22)
    
    Returns:
        paramiko.SSHClient object if successful, None otherwise
    """
    try:
        # Load private key
        private_key = paramiko.RSAKey.from_private_key_file(private_key_path)
        
        # Create SSH client
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.RejectPolicy())  # Strict host key checking
        
        # Connect to server
        ssh.connect(
            hostname=hostname,
            username=username,
            pkey=private_key,
            port=port,
            timeout=10  # Set connection timeout
        )
        
        return ssh
        
    except paramiko.AuthenticationException:
        print("Authentication failed, please check your credentials.")
        return None
    except paramiko.SSHException as e:
        print(f"SSH connection error: {str(e)}")
        return None
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None
    finally:
        # Ensure connection is closed
        if 'ssh' in locals() and ssh.get_transport() is not None:
            ssh.close()