import socket
import logging
from typing import Tuple

def create_secure_socket(port: int) -> Tuple[socket.socket, str]:
    """
    Creates a secure socket that listens on all interfaces for the specified port.
    
    Args:
        port: Port number to listen on
        
    Returns:
        Tuple containing (socket object, bound address)
        
    Raises:
        ValueError: If port is not a valid integer
        OSError: If socket creation fails
    """
    # Configure logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    
    # Validate port number
    if not isinstance(port, int) or port < 1 or port > 65535:
        raise ValueError("Port must be an integer between 1 and 65535")
    
    try:
        # Create socket with default IPv4 and TCP
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        # Set SO_REUSEADDR to avoid "Address already in use" errors
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        # Bind to all available interfaces
        sock.bind(('0.0.0.0', port))
        
        # Listen for connections
        sock.listen(5)
        
        # Get bound address
        bound_address = sock.getsockname()
        
        logger.info(f"Socket bound to {bound_address[0]}:{bound_address[1]}")
        
        return sock, bound_address[0]
        
    except socket.error as e:
        logger.error(f"Failed to create socket: {str(e)}")
        raise