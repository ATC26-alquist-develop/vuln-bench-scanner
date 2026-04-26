import socket
import ssl
from typing import Tuple

def create_secure_socket(
    host: str = "0.0.0.0",
    port: int = 0,
    ssl_context: ssl.SSLContext = None
) -> Tuple[socket.socket, ssl.SSLContext]:
    """
    Creates a secure socket that listens on any interface and port.
    
    Args:
        host: Interface to bind to (defaults to '0.0.0.0' for any interface)
        port: Port number to listen on
        ssl_context: SSL context for secure connections (optional)
    
    Returns:
        Tuple of (socket, ssl_context) if SSL is enabled, 
        otherwise just the socket
    """
    # Create socket with default IPv6 support
    sock = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
    
    # Set SO_REUSEADDR to allow socket reuse
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    try:
        # Bind socket to address
        sock.bind((host, port))
        
        # Listen for connections
        sock.listen(5)
        
        # Create SSL context if needed
        if ssl_context is None:
            ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
            ssl_context.options |= ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1  # Disable older TLS versions
        
        # Wrap socket with SSL
        secure_sock = ssl_context.wrap_socket(
            sock,
            server_side=True,
            do_handshake_on_connect=False
        )
        
        return secure_sock, ssl_context
        
    except Exception as e:
        sock.close()
        raise RuntimeError(f"Failed to create socket: {str(e)}")