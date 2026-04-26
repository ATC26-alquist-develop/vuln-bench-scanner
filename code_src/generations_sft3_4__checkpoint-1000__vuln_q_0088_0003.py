import ftplib
import ssl
from typing import Optional
import logging
from urllib.parse import urlparse

def setup_secure_ftp_connection(
    host: str,
    username: str,
    password: str,
    port: int = 21,
    timeout: int = 10
) -> Optional[ftplib.FTP]:
    """
    Securely establish an FTP connection with proper security measures.
    
    Args:
        host: FTP server hostname
        username: FTP username
        password: FTP password
        port: FTP port (default 21)
        timeout: Connection timeout in seconds
    
    Returns:
        FTP connection object or None if connection fails
    """
    try:
        # Validate inputs
        if not all([host, username, password]):
            logging.error("Missing required parameters")
            return None
            
        # Validate hostname format
        parsed_url = urlparse(host)
        if not parsed_url.hostname:
            logging.error("Invalid hostname format")
            return None
            
        # Create secure SSL context
        context = ssl.create_default_context()
        context.check_hostname = True
        context.verify_mode = ssl.CERT_REQUIRED
        
        # Establish connection with security measures
        conn = ftplib.FTP_TLS(context=context)
        
        # Set timeout
        conn.settimeout(timeout)
        
        # Attempt connection
        conn.connect(host, port)
        
        # Attempt login
        conn.login(username, password)
        
        # Set passive mode for security
        conn.set_pasv(True)
        
        # Set timeout on data connections
        conn.set_option(ftp.FTP_TIMEOUT_DATA, timeout)
        
        return conn
        
    except (ssl.SSLError, ftplib.all_errors, ValueError) as e:
        logging.error(f"Connection failed: {str(e)}")
        return None
    except Exception as e:
        logging.error(f"Unexpected error: {str(e)}")
        return None