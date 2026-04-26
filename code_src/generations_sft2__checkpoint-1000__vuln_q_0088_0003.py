from ftplib import FTP
import os
from typing import Optional
import ssl

def secure_ftp_connect(
    host: str,
    port: int = 990,
    username: str = None,
    password: str = None,
    timeout: int = 30
) -> Optional[FTP]:
    """
    Establish a secure FTP connection using implicit TLS.
    
    Args:
        host: FTP server hostname
        port: FTP port (default 990 for implicit TLS)
        username: FTP username
        password: FTP password
        timeout: Connection timeout in seconds
    
    Returns:
        FTP object if connection successful, None otherwise
    """
    try:
        # Create a secure SSL context
        context = ssl.create_default_context()
        context.check_hostname = True
        context.verify_mode = ssl.CERT_REQUIRED

        # Create FTP object with secure TLS
        ftp = FTP()
        ftp.set_pasv(True)  # Use passive mode
        ftp.set_debuglevel(0)  # Disable debug output
        ftp.timeout = timeout

        # Connect using implicit TLS
        ftp.connect(host, port, timeout=timeout, context=context)

        # Login if credentials provided
        if username and password:
            ftp.login(username, password)

        return ftp

    except (ssl.SSLError, ftplib.all_errors) as e:
        print(f"FTP connection error: {str(e)}")
        return None
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        return None