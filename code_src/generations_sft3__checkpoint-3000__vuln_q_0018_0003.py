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
        
        if not ip or port < 1 or port > 65535:
            raise ValueError("Invalid IP or port")
        
        # Create secure SSL context
        context = ssl.create_default_context()
        
        # Create socket with timeout
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(10)  # 10 second timeout
        
        # Wrap socket with SSL
        secure_sock = context.wrap_socket(
            sock,
            server_hostname=ip  # For hostname verification
        )
        
        try:
            # Connect with timeout
            secure_sock.connect((ip, port))
            logger.info(f"Successfully connected to {ip}:{port}")
            yield secure_sock
        finally:
            secure_sock.close()
    except (socket.error, ssl.SSLError) as e:
        logger.error(f"Failed to create socket: {str(e)}")
        raise

def send_data(secure_sock: ssl.SSLSocket, data: bytes) -> None:
    """
    Send data securely over the established socket connection.
    
    Args:
        secure_sock: Secure SSL socket connection
        data: Data to send (bytes)
    
    Raises:
        socket.error: If sending fails
    """
    try:
        secure_sock.sendall(data)
    except (socket.error, ssl.SSLError) as e:
        logger.error(f"Failed to send data: {str(e)}")
        raise