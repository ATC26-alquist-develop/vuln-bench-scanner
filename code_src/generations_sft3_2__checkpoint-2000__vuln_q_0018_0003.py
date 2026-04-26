import socket
import ssl
from typing import Tuple
import logging
from contextlib import contextmanager

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@contextmanager
def create_secure_socket(ip: str, port: int) -> ssl.SSLSocket:
    """
    Creates a secure SSL socket connection with proper error handling.
    
    Args:
        ip: Target IP address
        port: Target port number
    
    Returns:
        ssl.SSLSocket: Secure socket connection
    
    Raises:
        ValueError: If invalid IP or port is provided
        socket.error: If socket connection fails
    """
    try:
        # Validate input
        if not isinstance(ip, str) or not isinstance(port, int):
            raise ValueError("Invalid input types")
        
        if port < 1 or port > 65535:
            raise ValueError("Invalid port number")
            
        # Create SSL context with secure defaults
        context = ssl.create_default_context()
        context.check_hostname = True
        context.verify_mode = ssl.CERT_REQUIRED
        
        # Create socket and wrap with SSL
        sock = socket.create_connection((ip, port))
        secure_sock = context.wrap_socket(sock, 
                                          server_hostname=ip)
        
        logger.info(f"Secure connection established to {ip}:{port}")
        yield secure_sock
        
    except (socket.error, ssl.SSLError) as e:
        logger.error(f"Failed to create secure socket: {str(e)}")
        raise
        
    finally:
        try:
            secure_sock.close()
            logger.info("Secure socket closed")
        except Exception as e:
            logger.error(f"Error closing secure socket: {str(e)}")