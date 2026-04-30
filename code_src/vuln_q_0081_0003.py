```python
import paramiko
import os
import logging
from typing import Optional

def secure_ssh_connection(
    hostname: str,
    username: str,
    private_key_path: str,
    port: int = 22
) -> Optional[paramiko.SSHClient]:
    """
    Establish a secure SSH connection using Paramiko with proper security measures.
    
    Args:
        hostname: Remote host address
        username: Username for authentication
        private_key_path: Path to private key file
        port: SSH port (default: 22)
    
    Returns:
        SSHClient object if connection is successful, None otherwise
    """
    try:
        # Configure logging
        logging.basicConfig(level=logging.INFO)
        logger = logging.getLogger(__name__)

        # Load private key securely
        private_key = paramiko.RSAKey.from_private_key_file(private_key_path)
        
        # Create SSH client
        client = paramiko.SSHClient()
        client.load_system_host_keys()
        client.set_missing_host_key_policy(paramiko.RejectPolicy())  # Strict host key checking
        
        # Connect to host
        client.connect(
            hostname=hostname,
            username=username,
            pkey=private_key,
            port=port,
            timeout=10  # Connection timeout
        )
        
        logger.info(f"Successfully connected to {hostname}")
        return client

    except paramiko.AuthenticationException:
        logger.error("Authentication failed")
        return None
    except paramiko.SSHException as e:
        logger.error(f"SSH connection error: {str(e)}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return None
    finally:
        if 'client' in locals() and client.get_transport() and client.get_transport().is_active():
            client.close()
```