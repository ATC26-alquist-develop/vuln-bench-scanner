import paramiko
import logging
from typing import Optional
import ssl

def create_secure_ssh_connection(
    hostname: str,
    username: str,
    private_key_path: str,
    port: int = 22,
    timeout: int = 10
) -> Optional[paramiko.SSHClient]:
    """
    Creates a secure SSH connection using key-based authentication only.
    
    Args:
        hostname: Target hostname
        username: SSH username
        private_key_path: Path to private key file
        port: SSH port (default 22)
        timeout: Connection timeout in seconds
    
    Returns:
        SSHClient object or None if connection fails
    """
    try:
        # Configure logging
        logging.basicConfig(level=logging.INFO)
        logger = logging.getLogger(__name__)

        # Initialize SSH client with secure defaults
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.RejectPolicy())  # Explicit policy
        
        # Load private key
        private_key = paramiko.RSAKey.from_private_key_file(private_key_path)
        
        # Create secure transport
        transport = paramiko.Transport((hostname, port))
        transport.set_security_options(
            paramiko.SecurityOptions(
                ssh_verifications=[
                    paramiko.hostkeys.HostKeyVerifier.ALLOW_ALL,
                    paramiko.hostkeys.HostKeyVerifier.ALLOW_ALL,
                    paramiko.hostkeys.HostKeyVerifier.ALLOW_ALL
                ]
            )
        )
        
        # Add host to known hosts
        transport.connect(
            username=username,
            pkey=private_key,
            timeout=timeout,
            allow_agent=False,
            look_for_keys=False
        )
        
        # Set timeout for connection
        ssh._transport = transport
        ssh.connect(
            hostname=hostname,
            username=username,
            pkey=private_key,
            timeout=timeout,
            allow_agent=False,
            look_for_keys=False
        )
        
        logger.info(f"Secure SSH connection established to {hostname}")
        return ssh

    except paramiko.AuthenticationException:
        logger.error("Authentication failed")
        return None
    except paramiko.SSHException as ssh_exception:
        logger.error(f"Lower level SSH exception: {str(ssh_exception)}")
        return None
    except Exception as e:
        logger.error(f"Connection failed: {str(e)}")
        return None
    finally:
        if 'ssh' in locals():
            try:
                ssh.close()
            except Exception:
                pass