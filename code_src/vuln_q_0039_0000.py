import socket
import ssl
import logging
from typing import Tuple
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_secure_server(
    host: str = '127.0.0.1',  # Localhost by default
    port: int = 8443,
    cert_file: str = None,
    key_file: str = None
) -> ssl.SSLSocket:
    """
    Create a secure SSL server that listens on localhost by default.
    
    Args:
        host: Host to bind to (default: localhost)
        port: Port to listen on (default: 8443)
        cert_file: Path to SSL certificate file
        key_file: Path to SSL key file
        
    Returns:
        ssl.SSLSocket: Secure SSL socket
        
    Raises:
        ssl.SSLError: If SSL certificate/key issues
        OSError: If socket operations fail
    """
    # Validate inputs
    if not isinstance(host, str) or not isinstance(port, int):
        raise TypeError("Host must be str and port must be int")
    if port < 1 or port > 65535:
        raise ValueError("Port must be between 1 and 65535")
    
    # Create socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Set timeout to prevent hanging
    sock.settimeout(30)
    
    try:
        # Bind to localhost by default
        sock.bind((host, port))
        
        # Create SSL context
        context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        
        # Load certificates
        if cert_file and key_file:
            context.load_cert_chain(certfile=cert_file, keyfile=key_file)
        else:
            # Create self-signed cert if not provided
            context.load_default_certs()
        
        # Wrap socket with SSL
        secure_sock = context.wrap_socket(
            sock,
            server_side=True,
            do_handshake_on_connect=True
        )
        
        logger.info(f"Server started on {host}:{port}")
        return secure_sock
        
    except ssl.SSLError as e:
        logger.error(f"SSL error: {str(e)}")
        raise
    except OSError as e:
        logger.error(f"Socket error: {str(e)}")
        raise
    finally:
        if 'secure_sock' in locals():
            secure_sock.close()

# Example usage
if __name__ == "__main__":
    try:
        server_socket = create_secure_server()
        # Add your server logic here
        server_socket.close()
    except Exception as e:
        logger.error(f"Server error: {str(e)}")