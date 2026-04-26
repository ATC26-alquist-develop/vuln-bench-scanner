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
        ssl.SSLSocket: Secure SSL socket
        
    Raises:
        ValueError: If configuration parameters are invalid
        socket.error: If socket creation fails
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

    # Create secure SSL context
    context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
    context.check_hostname = True
    context.verify_mode = ssl.CERT_REQUIRED
    context.load_default_certs()

    # Create socket
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(config.timeout)
        
        # Wrap socket with SSL
        secure_sock = context.wrap_socket(
            sock,
            server_hostname=config.host
        )
        
        # Set connection timeout
        secure_sock.settimeout(config.timeout)
        
        # Set maximum message size
        secure_sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, config.max_size)
        
        return secure_sock
        
    except (socket.error, ssl.SSLError) as e:
        logging.error(f"Failed to create secure socket: {str(e)}")
        raise

def send_data(secure_sock: ssl.SSLSocket, data: bytes) -> None:
    """
    Send data securely over the established SSL connection.
    
    Args:
        secure_sock: SSL socket object
        data: Data to send (bytes)
        
    Raises:
        ValueError: If data is invalid
        socket.error: If sending fails
    """
    if not isinstance(data, bytes):
        raise ValueError("Data must be bytes")
    
    try:
        secure_sock.sendall(data)
    except (socket.error, ssl.SSLError) as e:
        logging.error(f"Failed to send data: {str(e)}")
        raise

def main() -> None:
    try:
        # Example usage
        config = SecureSocketConfig(
            host="example.com",
            port=443
        )
        
        with create_secure_socket(config) as secure_sock:
            # Establish connection
            secure_sock.connect((config.host, config.port))
            
            # Send data
            data = b"Hello, secure world!"
            send_data(secure_sock, data)
            
            # Receive response (example)
            response = secure_sock.recv(1024)
            print(f"Received: {response.decode('utf-8')}")
            
    except Exception as e:
        logging.error(f"Error in main: {str(e)}")
        raise

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()