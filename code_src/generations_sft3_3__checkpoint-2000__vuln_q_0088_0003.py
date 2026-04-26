import ftplib
import ssl
from typing import Optional
import logging
from urllib.parse import urlparse

def secure_ftp_connection(
    hostname: str,
    username: str,
    password: str,
    port: int = 21,
    timeout: int = 30
) -> Optional[ftplib.FTP]:
    """
    Establishes a secure FTP connection using TLS.
    
    Args:
        hostname: FTP server hostname
        username: FTP username
        password: FTP password
        port: FTP server port (default 21)
        timeout: Connection timeout in seconds
    
    Returns:
        FTP connection object or None if connection fails
    """
    try:
        # Validate hostname
        parsed_url = urlparse(hostname)
        if not parsed_url.hostname:
            logging.error("Invalid hostname provided")
            return None
            
        # Create secure SSL context
        context = ssl.create_default_context()
        context.check_hostname = True
        context.verify_mode = ssl.CERT_REQUIRED
        
        # Establish connection with TLS
        conn = ftplib.FTP_TLS(
            hostname=hostname,
            timeout=timeout,
            context=context
        )
        
        # Attempt to upgrade to TLS
        conn.prot_p()
        
        # Login with provided credentials
        conn.login(username, password)
        
        # Return connection object
        return conn
        
    except (ftplib.all_errors, ssl.SSLError, ValueError) as e:
        logging.error(f"Connection failed: {str(e)}")
        return None
    except Exception as e:
        logging.error(f"Unexpected error: {str(e)}")
        return None