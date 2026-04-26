import ssl
import socket
from typing import Optional

def create_secure_connection(host: str, port: int = 443) -> Optional[ssl.SSLSocket]:
    """
    Establishes a secure connection to a remote server using HTTPS.
    
    Args:
        host: The hostname of the server
        port: The port number (default: 443 for HTTPS)
    
    Returns:
        A secure SSL socket if connection is successful, None otherwise
    """
    try:
        # Create a secure SSL context
        context = ssl.create_default_context()
        
        # Enable certificate verification
        context.verify_mode = ssl.CERT_REQUIRED
        context.check_hostname = True
        
        # Create a socket and wrap it with SSL
        with socket.create_connection((host, port)) as sock:
            with context.wrap_socket(sock, server_hostname=host) as secure_sock:
                return secure_sock
                
    except (ssl.SSLError, socket.error) as e:
        # Log the error here if needed
        return None