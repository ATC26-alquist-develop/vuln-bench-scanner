import ssl
import socket
from typing import Optional

def create_secure_connection(host: str, port: int, timeout: float = 10.0) -> Optional[ssl.SSLSocket]:
    """
    Establishes a secure connection to a remote server using HTTPS.
    
    Args:
        host: The hostname or IP address of the server
        port: The port number to connect to
        timeout: Connection timeout in seconds
        
    Returns:
        SSL socket object if connection is successful, None otherwise
        
    Raises:
        ssl.SSLError: If SSL/TLS handshake fails
        socket.error: If connection fails
    """
    try:
        # Create a secure SSL context
        context = ssl.create_default_context()
        
        # Enable certificate verification
        context.verify_mode = ssl.CERT_REQUIRED
        context.check_hostname = True
        
        # Create a socket and wrap it with SSL
        sock = socket.create_connection((host, port), timeout=timeout)
        ssl_sock = context.wrap_socket(sock, server_hostname=host)
        
        return ssl_sock
        
    except (ssl.SSLError, socket.error) as e:
        # Log error here if needed
        return None