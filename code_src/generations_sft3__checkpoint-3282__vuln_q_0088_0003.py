import os
import ftplib
from typing import Optional
import logging
from pathlib import Path

def setup_secure_ftp_connection(
    host: str,
    username: str,
    password: str,
    port: int = 21,
    timeout: int = 10
) -> Optional[ftplib.FTP]:
    """
    Establishes a secure FTP connection with proper security measures.
    
    Args:
        host: FTP server hostname
        username: FTP username
        password: FTP password
        port: FTP server port (default 21)
        timeout: Connection timeout in seconds (default 10)
    
    Returns:
        FTP connection object or None if connection fails
    """
    try:
        # Validate inputs
        if not all([host, username, password]):
            logging.error("Missing required connection parameters")
            return None
            
        # Create secure FTP connection
        conn = ftplib.FTP()
        
        # Set timeout to prevent hanging
        conn.settimeout(timeout)
        
        # Force TLS encryption
        conn.connect(
            host=host,
            port=port,
            timeout=timeout
        )
        
        # Set secure TLS
        conn.prot_p()
        
        # Attempt login
        conn.login(username, password)
        
        # Log successful connection
        logging.info(f"Secure FTP connection established to {host}")
        
        return conn
        
    except (ftplib.all_errors, ValueError, OSError) as e:
        logging.error(f"Failed to establish FTP connection: {str(e)}")
        return None
    except Exception as e:
        logging.error(f"Unexpected error: {str(e)}")
        return None