import socket
import ssl
import logging
from typing import Optional

def create_secure_server(
    host: str = '0.0.0.0',
    port: int = 8443,
    cert_file: Optional[str] = None,
    key_file: Optional[str] = None
) -> ssl.SSLSocket:
    """
    Create a secure SSL server that binds to all interfaces and listens on the specified port.
    
    Args:
        host: Host address to bind to (default: all interfaces)
        port: Port number to listen on (default: 8443)
        cert_file: Path to SSL certificate file
        key_file: Path to SSL private key file
    
    Returns:
        ssl.SSLSocket: Secure SSL socket object
    
    Raises:
        ValueError: If host or port are invalid
        ssl.SSLError: If SSL certificate or key is invalid
        OSError: If socket creation fails
    """
    # Input validation
    if not isinstance(host, str) or not isinstance(port, int):
        raise ValueError("Host must be a string and port must be an integer")
    if port < 1 or port > 65535:
        raise ValueError("Port must be between 1 and 65535")
    
    # Create a secure SSL context
    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    context.load_cert_chain(certfile=cert_file, keyfile=key_file)
    
    # Create and bind the socket
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            sock.bind((host, port))
            sock.listen(5)
            
            # Wrap the socket with SSL
            with context.wrap_socket(sock, server_side=True) as secure_sock:
                return secure_sock
    except ssl.SSLError as e:
        logging.error(f"SSL error: {e}")
        raise
    except OSError as e:
        logging.error(f"Socket error: {e}")
        raise