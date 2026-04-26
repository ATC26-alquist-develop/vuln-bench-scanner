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
        raise ValueError("IP must be string and port must be integer")
    
    if port < 1 or port > 65535:
        raise ValueError("Port must be between 1 and 65535")

    try:
        # Create secure socket with default TLS configuration
        sock = socket.create_connection((ip, port))
        
        # Wrap socket with SSL/TLS
        context = ssl.create_default_context()
        secure_sock = context.wrap_socket(sock, 
                                         server_hostname=ip)
        
        yield secure_sock
        
    except socket.error as e:
        logger.error(f"Socket connection failed: {e}")
        raise
    except ssl.SSLError as e:
        logger.error(f"SSL error: {e}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise
    finally:
        try:
            secure_sock.close()
        except:
            pass