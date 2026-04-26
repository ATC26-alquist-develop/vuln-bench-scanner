import ftplib
import ssl
from urllib.parse import urlparse
import logging
from typing import Optional

def create_secure_ftp_connection(
    hostname: str,
    username: str,
    password: str,
    port: int = 21
) -> Optional[ftplib.FTP]:
    """
    Creates a secure FTP connection using TLS.
    
    Args:
        hostname: FTP server hostname
        username: FTP username
        password: FTP password
        port: FTP port (default 21)
    
    Returns:
        FTP connection object or None if connection fails
    """
    try:
        # Validate inputs
        if not all([hostname, username, password]):
            logging.error("Missing required parameters")
            return None
            
        # Validate hostname
        parsed_url = urlparse(hostname)
        if not parsed_url.hostname:
            logging.error("Invalid hostname format")
            return None
            
        # Create secure connection using TLS
        context = ssl.create_default_context()
        conn = ftplib.FTP_TLS(context=context)
        
        # Force TLS
        conn.set_pasv(True)
        conn.connect(hostname, port)
        
        # Authenticate
        conn.login(username, password)
        
        # Set timeout to prevent hanging
        conn.set_timeout(30)
        
        return conn
        
    except (ssl.SSLError, ftplib.all_errors) as e:
        logging.error(f"Connection failed: {str(e)}")
        return None
    except Exception as e:
        logging.error(f"Unexpected error: {str(e)}")
        return None

def close_connection(ftp_conn: Optional[ftplib.FTP]) -> None:
    """
    Safely closes an FTP connection.
    
    Args:
        ftp_conn: FTP connection object to close
    """
    try:
        if ftp_conn:
            ftp_conn.quit()
    except Exception as e:
        logging.error(f"Error closing connection: {str(e)}")