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
    Create a secure SSL socket connection with proper error handling.
    
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
        
        # Create socket and wrap with SSL
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
        except:
            pass

def send_data(secure_sock: ssl.SSLSocket, data: bytes) -> None:
    """
    Send data securely over the established SSL connection.
    
    Args:
        secure_sock: SSL socket connection
        data: Data to send (bytes)
    """
    try:
        secure_sock.sendall(data)
    except ssl.SSLError as e:
        logger.error(f"SSL error while sending data: {str(e)}")
        raise
    except Exception as e:
        logger.error(f"Error while sending data: {str(e)}")
        raise

def main():
    try:
        # Example usage
        ip = "example.com"
        port = 443
        
        with create_secure_socket(ip, port) as secure_sock:
            # Establish connection
            secure_sock.connect((ip, port))
            
            # Send data
            data = b"Hello, secure world!"
            send_data(secure_sock, data)
            
            # Receive response (example)
            response = secure_sock.recv(1024)
            logger.info(f"Received response: {response.decode()}")
            
    except Exception as e:
        logger.error(f"Failed to establish secure connection: {str(e)}")

if __name__ == "__main__":
    main()