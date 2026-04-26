import socket
import ssl
import logging
from typing import Optional

def create_secure_connection(host: str, port: int, ca_cert_path: Optional[str] = None) -> Optional[ssl.SSLSocket]:
    """
    Creates a secure SSL socket connection to the specified host and port.
    
    Args:
        host: The hostname to connect to
        port: The port number to connect to
        ca_cert_path: Optional path to CA certificate file for certificate verification
    
    Returns:
        SSLSocket object if connection is successful, None otherwise
    
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

        # Create socket and wrap it with SSL
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        secure_sock = context.wrap_socket(sock, server_hostname=host)

        # Connect to the server
        secure_sock.connect((host, port))
        logger.info(f"Successfully connected to {host}:{port}")
        return secure_sock

    except (ssl.SSLError, socket.error) as e:
        logger.error(f"Failed to create secure connection: {str(e)}")
        return None

def close_connection(ssl_socket: Optional[ssl.SSLSocket]) -> None:
    """
    Closes the SSL socket connection properly.
    
    Args:
        ssl_socket: SSL socket object to close
    
    Raises:
        ssl.SSLError: If SSL shutdown fails
        socket.error: If socket close fails
    """
    if ssl_socket is None:
        return

    try:
        ssl_socket.shutdown(socket.SHUT_RDWR)
        ssl_socket.close()
        logging.info("SSL socket connection closed successfully")
    except (ssl.SSLError, socket.error) as e:
        logging.error(f"Failed to close SSL socket: {str(e)}")

# Example usage
if __name__ == "__main__":
    HOST = "example.com"
    PORT = 443
    CA_CERT = "/path/to/ca_cert.pem"

    ssl_socket = create_secure_connection(HOST, PORT, CA_CERT)
    if ssl_socket:
        # Perform operations with the secure connection
        pass
    else:
        print("Failed to create secure connection")
    
    # Always close the connection
    close_connection(ssl_socket)