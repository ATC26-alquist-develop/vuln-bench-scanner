import socket
import ssl
import logging
from typing import Optional

def create_secure_connection(host: str, port: int, ca_cert_path: Optional[str] = None) -> Optional[ssl.SSLSocket]:
    """
    Creates a secure SSL socket connection with proper error handling and logging.
    
    Args:
        host: Target hostname
        port: Target port
        ca_cert_path: Optional path to CA certificate file
    
    Returns:
        SSLSocket object if connection successful, None otherwise
    
    Raises:
        ssl.SSLError: If SSL/TLS handshake fails
        socket.error: If socket connection fails
    """
    try:
        # Configure logging
        logging.basicConfig(level=logging.INFO)
        logger = logging.getLogger(__name__)

        # Create SSL context with secure defaults
        context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH, cafile=ca_cert_path)
        
        # Enable certificate verification
        context.verify_mode = ssl.CERT_REQUIRED
        context.check_hostname = True

        # Create socket and wrap with SSL
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        with context.wrap_socket(sock, server_hostname=host) as secure_sock:
            logger.info(f"Attempting connection to {host}:{port}")
            secure_sock.connect((host, port))
            logger.info("Connection established successfully")
            return secure_sock

    except ssl.SSLError as e:
        logger.error(f"SSL error occurred: {e}")
    except socket.error as e:
        logger.error(f"Socket error occurred: {e}")
    except Exception as e:
        logger.error(f"Unexpected error occurred: {e}")
    
    return None

def close_connection(sock: Optional[ssl.SSLSocket]) -> None:
    """
    Safely closes the SSL socket connection.
    
    Args:
        sock: SSL socket object to close
    """
    if sock is not None:
        try:
            sock.close()
            logging.info("Connection closed successfully")
        except Exception as e:
            logging.error(f"Error closing connection: {e}")

# Example usage
if __name__ == "__main__":
    connection = create_secure_connection("example.com", 443)
    if connection:
        try:
            # Perform operations with the connection
            pass
        finally:
            close_connection(connection)