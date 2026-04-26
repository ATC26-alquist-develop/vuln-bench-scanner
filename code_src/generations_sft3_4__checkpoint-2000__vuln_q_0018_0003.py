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
    try:
        # Validate inputs
        if not isinstance(ip, str) or not isinstance(port, int):
            raise ValueError("Invalid input types")
        if port < 1 or port > 65535:
            raise ValueError("Invalid port number")
            
        # Create secure SSL context
        context = ssl.create_default_context()
        context.check_hostname = True
        context.verify_mode = ssl.CERT_REQUIRED
        
        # Create socket and wrap with SSL
        sock = socket.create_connection((ip, port))
        secure_sock = context.wrap_socket(sock, 
                                         server_hostname=ip)
        
        logger.info(f"Successfully connected to {ip}:{port}")
        yield secure_sock
        
    except socket.error as e:
        logger.error(f"Socket connection failed: {str(e)}")
        raise
    except ssl.SSLError as e:
        logger.error(f"SSL handshake failed: {str(e)}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise
    finally:
        try:
            secure_sock.close()
            logger.info("Socket connection closed")
        except Exception:
            pass