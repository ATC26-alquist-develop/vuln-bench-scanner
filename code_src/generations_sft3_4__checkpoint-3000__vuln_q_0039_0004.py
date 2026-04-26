import socket
import ssl
from typing import Tuple
import logging

def create_secure_socket(
    host: str = "0.0.0.0",
    port: int = 0,
    cert_path: str = None,
    key_path: str = None,
    ca_path: str = None
) -> Tuple[socket.socket, ssl.SSLContext]:
    """
    Creates a secure socket that listens on any interface and supports TLS.
    
    Args:
        host: Interface to bind to (defaults to '0.0.0.0' for any interface)
        port: Port number to listen on
        cert_path: Path to SSL certificate file
        key_path: Path to SSL private key file
        ca_path: Path to CA certificate file for verification
        
    Returns:
        Tuple of (socket, ssl context)
    """
    try:
        # Configure logging
        logging.basicConfig(level=logging.INFO)
        logger = logging.getLogger(__name__)

        # Create socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        # Set socket options for SO_REUSEADDR
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        # Bind socket
        sock.bind((host, port))
        
        # Create SSL context
        ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        
        # Enable TLS
        if cert_path and key_path:
            ssl_context.load_cert_chain(certfile=cert_path, keyfile=key_path)
            
        if ca_path:
            ssl_context.load_verify_locations(cafile=ca_path)
            
        ssl_context.verify_mode = ssl.CERT_REQUIRED
        ssl_context.check_hostname = True
        
        # Wrap socket with SSL
        secure_sock = ssl_context.wrap_socket(
            sock,
            server_side=True,
            do_handshake_on_connect=True
        )
        
        logger.info(f"Secure socket created on {host}:{port}")
        return secure_sock, ssl_context
        
    except Exception as e:
        logger.error(f"Error creating secure socket: {str(e)}")
        raise