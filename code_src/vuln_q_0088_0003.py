import os
import paramiko
from typing import Optional
import ssl

def create_secure_ftp_connection(
    hostname: str,
    username: str,
    password: str,
    port: int = 990,  # Default secure FTP port
    timeout: int = 30
) -> Optional[paramiko.SFTPClient]:
    """
    Create a secure SFTP connection to an FTP server.
    
    Args:
        hostname: FTP server hostname
        username: Username for authentication
        password: Password for authentication
        port: FTP port (default 990 for implicit TLS)
        timeout: Connection timeout in seconds
    
    Returns:
        SFTPClient object if connection successful, None otherwise
    """
    try:
        # Create a secure SSL context
        context = ssl.create_default_context()
        context.options |= ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1  # Disable older TLS versions
        
        # Create SSH client with secure defaults
        ssh = paramiko.SSHClient()
        ssh.load_system_host_keys()
        ssh.set_missing_host_key_policy(paramiko.RejectPolicy())  # Strict host key checking
        
        # Connect with timeout and secure options
        ssh.connect(
            hostname=hostname,
            port=port,
            username=username,
            password=password,
            timeout=timeout,
            allow_agent=False,
            look_for_keys=False,
            sock_timeout=timeout
        )
        
        # Create SFTP client from secure SSH connection
        sftp = ssh.open_sftp()
        return sftp
        
    except (paramiko.AuthenticationException, paramiko.SSHException, 
            paramiko.SFTPError, socket.error, OSError) as e:
        print(f"Connection failed: {str(e)}")
        return None
    finally:
        if 'sftp' in locals() and sftp.is_active():
            sftp.close()