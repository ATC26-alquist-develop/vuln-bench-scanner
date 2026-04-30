import paramiko
from paramiko import SSHException
import os

def create_ssh_client(hostname, port, username, private_key_path):
    """
    Create and return an SSH client object.
    
    Args:
        hostname (str): Remote host
        port (int): SSH port
        username (str): Username for authentication
        private_key_path (str): Path to private key file
    
    Returns:
        paramiko.SSHClient: Configured SSH client object
    
    Raises:
        SSHException: If SSH connection fails
        FileNotFoundError: If private key file not found
    """
    # Load private key
    try:
        private_key = paramiko.RSAKey.from_private_key_file(private_key_path)
    except FileNotFoundError:
        raise FileNotFoundError(f"Private key file not found: {private_key_path}")
    
    # Create SSH client
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.RejectPolicy())  # Security: Reject unknown hosts
    
    try:
        client.connect(
            hostname=hostname,
            port=port,
            username=username,
            pkey=private_key,
            timeout=30  # Timeout after 30 seconds
        )
    except SSHException as e:
        raise SSHException(f"SSH connection failed: {str(e)}")
    
    return client

def execute_ssh_command(ssh_client, command):
    """
    Execute a command on the remote host.
    
    Args:
        ssh_client (paramiko.SSHClient): Configured SSH client
        command (str): Command to execute
    
    Returns:
        str: Command output
    
    Raises:
        SSHException: If command execution fails
    """
    stdin, stdout, stderr = ssh_client.exec_command(
        command,
        get_pty=False,  # Don't use pseudo-terminal
        timeout=30  # Timeout after 30 seconds
    )
    
    return stdout.read().decode('utf-8').strip()