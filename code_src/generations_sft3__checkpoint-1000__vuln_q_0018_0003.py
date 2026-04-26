```python
import socket
import ssl
from typing import Tuple
import logging
from dataclasses import dataclass

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class SecureSocketConfig:
    """Secure socket configuration"""
    host: str
    port: int
    timeout: float = 5.0
    max_size: int = 1024 * 1024  # 1MB max packet size

def create_secure_socket(config: SecureSocketConfig) -> ssl.SSLSocket:
    """
    Create a secure SSL socket connection to the specified host and port.
    
    Args:
        config: SecureSocketConfig object containing connection details
        
    Returns:
        ssl.SSLSocket: Secure SSL socket object
        
    Raises:
        ValueError: If configuration is invalid
        socket.error: If socket creation fails
    """
    try:
        # Validate configuration
        if not isinstance(config.host, str) or not config.host:
            raise ValueError("Invalid host")
        if not isinstance(config.port, int) or config.port <= 0 or config.port > 65535:
            raise ValueError("Invalid port")
        if not isinstance(config.timeout, (int, float)) or config.timeout <= 0:
            raise ValueError("Invalid timeout")
        if not isinstance(config.max_size, int) or config.max_size <= 0:
            raise ValueError("Invalid max packet size")

        # Create SSL context
        context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
        context.check_hostname = True
        context.verify_mode = ssl.CERT_REQUIRED

        # Create socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        # Set timeout
        sock.settimeout(config.timeout)
        
        # Wrap socket with SSL
        secure_sock = context.wrap_socket(
            sock,
            server_hostname=config.host
        )
        
        # Set connection timeout
        secure_sock.settimeout(config.timeout)
        
        # Set maximum packet size
        secure_sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, config.max_size)
        
        # Connect
        secure_sock.connect((config.host, config.port))
        
        logger.info(f"Secure connection established to {config.host}:{config.port}")
        return secure_sock

    except (socket.error, ValueError) as e:
        logger.error(f"Failed to create secure socket: {str(e)}")
        raise

def send_data(secure_sock: ssl.SSLSocket, data: bytes) -> None:
    """
    Send data securely over the established SSL socket.
    
    Args:
        secure_sock: SSL socket object
        data: Data to send (bytes)
        
    Raises:
        ValueError: If data is invalid
        ssl.SSLError: If SSL handshake fails
        socket.error: If socket operation fails
    """
    if not isinstance(data, bytes):
        raise ValueError("Data must be bytes")
    
    try:
        # Send data with proper size checking
        total_sent = 0
        while total_sent < len(data):
            sent = secure_sock.send(data[total_sent:])
            if sent == 0:
                raise socket.error("Socket connection broken")
            total_sent += sent
            
        logger.info(f"Data sent successfully: {len(data)} bytes")
        
    except (socket.error, ssl.SSLError) as e:
        logger.error(f"Failed to send data: {str(e)}")
        raise

def main():
    try:
        # Example usage
        config = SecureSocketConfig(
            host="example.com",
            port=443,
            timeout=5.0,
            max_size=1024 * 1024
        )
        
        secure_sock = create_secure_socket(config)
        
        # Example data
        data_to_send = b"Hello