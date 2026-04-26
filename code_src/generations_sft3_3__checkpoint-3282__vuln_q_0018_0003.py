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
        ssl.SSLError: If SSL/TLS handshake fails
    """
    # Input validation
    if not isinstance(ip, str) or not isinstance(port, int):
        raise ValueError("Invalid input types")
    
    if not ip or not port:
        raise ValueError("IP and port cannot be empty")
    
    if port < 1 or port > 65535:
        raise ValueError("Invalid port number")

    try:
        # Create a secure SSL context
        context = ssl.create_default_context()
        
        # Create socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        # Wrap socket with SSL
        secure_sock = context.wrap_socket(
            sock,
            server_hostname=ip  # For hostname verification
        )
        
        # Connect
        secure_sock.connect((ip, port))
        
        logger.info(f"Successfully connected to {ip}:{port}")
        yield secure_sock
        
    except socket.error as e:
        logger.error(f"Socket error occurred: {e}")
        raise
    except ssl.SSLError as e:
        logger.error(f"SSL error occurred: {e}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error occurred: {e}")
        raise
    finally:
        try:
            secure_sock.close()
            logger.info("Socket connection closed")
        except Exception:
            pass  # Already closed or exception occurred