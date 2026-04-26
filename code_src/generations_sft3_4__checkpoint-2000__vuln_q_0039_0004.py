import socket
import logging
from typing import Tuple

def create_secure_socket(port: int, timeout: int = 5) -> Tuple[socket.socket, str]:
    """
    Creates a secure socket that listens on all interfaces for the specified port.
    
    Args:
        port: Port number to listen on
        timeout: Connection timeout in seconds
    
    Returns:
        Tuple containing (socket object, bound address)
    """
    try:
        # Create a TCP socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        # Set socket options for security
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        # Bind to all available interfaces
        sock.bind(('0.0.0.0', port))
        
        # Set timeout
        sock.settimeout(timeout)
        
        # Listen for connections
        sock.listen(5)
        
        # Get bound address
        bound_address = sock.getsockname()[0]
        
        return sock, bound_address
        
    except socket.error as e:
        logging.error(f"Failed to create socket: {e}")
        raise
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        raise