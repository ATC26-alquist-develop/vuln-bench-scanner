import paramiko
from paramiko import SSHException
import os
import logging

def create_ssh_client(hostname, username, key_path):
    """
    Create a secure SSH client connection.
    
    Args:
        hostname (str): SSH server hostname
        username (str): SSH username
        key_path (str): Path to private key file
    
    Returns:
        paramiko.SSHClient: Configured SSH client object
    
    Raises:
        ValueError: If hostname, username, or key_path are invalid
        SSHException: If SSH connection fails
    """
    # Input validation
    if not all([hostname, username, key_path]):
        raise ValueError("Hostname, username, and key path are required")
    
    if not os.path.isfile(key_path):
        raise ValueError("Key file does not exist")
    
    # Create SSH client
    ssh = paramiko.SSHClient()
    ssh.load_system_host_keys()
    ssh.set_missing_host_key_policy(paramiko.RejectPolicy())  # Strict host key checking
    
    try:
        # Connect using key-based authentication
        ssh.connect(
            hostname=hostname,
            username=username,
            key_filename=key_path,
            timeout=10  # Set connection timeout
        )
    except SSHException as e:
        logging.error(f"SSH connection failed: {e}")
        raise
    
    return ssh

def execute_ssh_command(ssh, command):
    """
    Execute a command on the SSH server securely.
    
    Args:
        ssh (paramiko.SSHClient): Configured SSH client object
        command (str): Command to execute
    
    Returns:
        str: Command output
    
    Raises:
        SSHException: If command execution fails
    """
    try:
        # Execute command securely
        stdin, stdout, stderr = ssh.exec_command(command, get_pty=False)
        return stdout.read().decode().strip()
    except SSHException as e:
        logging.error(f"Command execution failed: {e}")
        raise