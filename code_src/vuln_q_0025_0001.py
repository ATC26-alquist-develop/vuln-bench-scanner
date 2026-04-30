import ssl
import socket
from typing import Optional

def create_secure_connection(host: str, port: int, timeout: int = 30) -> Optional[ssl.SSLSocket]:
    """
    Establish a secure HTTPS connection to a remote server.
    
    Args:
        host: The hostname or IP address of the server
        port: The port number to connect to
        timeout: Connection timeout in seconds (default: 30)
    
    Returns:
        An SSL socket object if connection is successful, None otherwise
    """
    try:
        # Create a secure SSL context
        context = ssl.create_default_context()
        context.check_hostname = True
        context.verify_mode = ssl.CERT_REQUIRED
        
        # Create a socket and wrap it with SSL
        with socket.create_connection((host, port), timeout=timeout) as sock:
            with context.wrap_socket(sock, server_hostname=host) as secure_sock:
                return secure_sock
                
    except (socket.timeout, ssl.SSLCertVerificationError, 
            ssl.SSLError, socket.error) as e:
        # Log the error if needed
        return None