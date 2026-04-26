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
        # Validate input parameters
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
        
        # Set security options
        conn.prot_p()  # Enable passive mode
        conn.login(username, password)
        
        # Verify connection
        if not conn.getwelcome():
            logging.error("Failed to connect to FTP server")
            conn.quit()
            return None
            
        return conn
        
    except (ssl.SSLError, ftplib.all_errors, Exception) as e:
        logging.error(f"Connection failed: {str(e)}")
        return None
    finally:
        # Ensure connection is closed
        if 'conn' in locals() and conn:
            try:
                conn.quit()
            except Exception:
                pass