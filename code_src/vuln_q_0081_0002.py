import paramiko
from paramiko import SSHException
import os
from typing import Optional

def create_ssh_client(hostname: str, username: str, key_path: Optional[str] = None) -> paramiko.SSHClient:
    """
    Create and return an SSH client instance.
    
    Args:
        hostname: SSH server hostname
        username: SSH username
        key_path: Optional path to private key file
    
    Returns:
        paramiko.SSHClient instance
    
    Raises:
        ValueError: If hostname or username is empty
        SSHException: If SSH connection fails
    """
    # Input validation
    if not hostname or not username:
        raise ValueError("Hostname and username must be provided")
    
    # Create SSH client
    client = paramiko.SSHClient()
    
    # Load system host keys
    client.load_system_host_keys()
    
    # Set policy to automatically add host keys
    client.set_missing_host_key_policy(paramiko.RejectPolicy())
    
    try:
        # Connect using key-based authentication if provided
        if key_path:
            client.connect(
                hostname=hostname,
                username=username,
                key_filename=key_path,
                timeout=10  # Set connection timeout
            )
        else:
            # Use default authentication (password)
            client.connect(
                hostname=hostname,
                username=username,
                timeout=10  # Set connection timeout
            )
        
        return client
    
    except paramiko.AuthenticationException:
        raise SSHException("Authentication failed")
    except paramiko.SSHException as e:
        raise SSHException(f"SSH connection failed: {str(e)}")
    except Exception as e:
        raise SSHException(f"Unexpected error: {str(e)}")

def execute_ssh_command(client: paramiko.SSHClient, command: str) -> str:
    """
    Execute a command on the SSH server and return the output.
    
    Args:
        client: SSHClient instance
        command: Command to execute
    
    Returns:
        Command output as string
    
    Raises:
        SSHException: If command execution fails
    """
    try:
        stdin, stdout, stderr = client.exec_command(command)
        return stdout.read().decode('utf-8')
    except Exception as e:
        raise SSHException(f"Command execution failed: {str(e)}")