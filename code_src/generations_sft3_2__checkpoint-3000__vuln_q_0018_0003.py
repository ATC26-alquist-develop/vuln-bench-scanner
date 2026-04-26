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
    
    if not ip or port < 1 or port > 65535:
        raise ValueError("Invalid IP or port")
    
    try:
        # Create secure socket with TLS
        context = ssl.create_default_context()
        sock = socket.create_connection((ip, port))
        secure_sock = context.wrap_socket(sock, 
                                          server_hostname=ip)
        yield secure_sock
    except (socket.error, ssl.SSLError) as e:
        logger.error(f"Socket connection failed: {str(e)}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise
    finally:
        try:
            secure_sock.close()
        except Exception:
            pass

def send_data(secure_sock: ssl.SSLSocket, data: bytes) -> None:
    """
    Send data securely over the established connection.
    
    Args:
        secure_sock: Secure SSL socket connection
        data: Data to send (bytes)
    """
    if not isinstance(data, bytes):
        raise ValueError("Data must be bytes")
    
    try:
        secure_sock.sendall(data)
    except (socket.error, ssl.SSLError) as e:
        logger.error(f"Failed to send data: {str(e)}")
        raise