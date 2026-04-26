import socket
import ssl
from typing import Tuple
import logging
from dataclasses import dataclass

@dataclass
class SecureSocketConfig:
    """Secure socket configuration with validated parameters"""
    host: str
    port: int
    timeout: float = 10.0
    max_size: int = 1024 * 1024  # 1MB max message size

def create_secure_socket(config: SecureSocketConfig) -> ssl.SSLSocket:
    """
    Creates a secure SSL socket connection with proper validation and security measures.
    
    Args:
        config: SecureSocketConfig object with validated parameters
        
    Returns:
        ssl.SSLSocket: Secure SSL socket connection
        
    Raises:
        ValueError: If configuration parameters are invalid
        socket.error: If socket connection fails
    """
    # Input validation
    if not isinstance(config.host, str) or not config.host:
        raise ValueError("Invalid host parameter")
    if not isinstance(config.port, int) or config.port < 1 or config.port > 65535:
        raise ValueError("Invalid port parameter")
    if not isinstance(config.timeout, (int, float)) or config.timeout <= 0:
        raise ValueError("Invalid timeout parameter")
    if not isinstance(config.max_size, int) or config.max_size <= 0:
        raise ValueError("Invalid max_size parameter")

    # Create socket
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error as e:
        logging.error(f"Failed to create socket: {e}")
        raise

    try:
        # Set timeout
        sock.settimeout(config.timeout)
        
        # Create SSL context
        context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
        context.check_hostname = True
        context.verify_mode = ssl.CERT_REQUIRED
        
        # Wrap socket with SSL
        secure_sock = context.wrap_socket(
            sock,
            server_hostname=config.host
        )
        
        # Set connection timeout
        secure_sock.settimeout(config.timeout)
        
        # Set max message size
        secure_sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, config.max_size)
        
        return secure_sock
        
    except ssl.SSLError as e:
        logging.error(f"SSL error: {e}")
        raise
    except socket.error as e:
        logging.error(f"Socket error: {e}")
        raise
    finally:
        if 'sock' in locals() and not sock.closed:
            sock.close()