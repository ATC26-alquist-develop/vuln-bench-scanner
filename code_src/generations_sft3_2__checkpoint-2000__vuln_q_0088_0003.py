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
        context.check_hostname = True
        context.verify_mode = ssl.CERT_REQUIRED
        
        # Create connection with TLS
        conn = ftplib.FTP_TLS(
            hostname=hostname,
            port=port,
            context=context
        )
        
        # Attempt to login
        conn.login(username, password)
        
        # Set passive mode for security
        conn.set_pasv(True)
        
        return conn
        
    except (ssl.SSLError, ftplib.all_errors) as e:
        logging.error(f"Connection failed: {str(e)}")
        return None
    except Exception as e:
        logging.error(f"Unexpected error: {str(e)}")
        return None