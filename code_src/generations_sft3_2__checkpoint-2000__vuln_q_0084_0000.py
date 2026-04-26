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
        ca_cert_path: Optional path to CA certificate file for verification
    
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
        context.options |= ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1  # Disable older TLS versions
        context.set_ciphers('ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384')
        
        # Create socket and wrap with SSL
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        secure_sock = context.wrap_socket(sock, server_hostname=host)
        
        # Connect to the server
        secure_sock.connect((host, port))
        logger.info(f"Successfully connected to {host}:{port}")
        return secure_sock
        
    except (ssl.SSLError, socket.error) as e:
        logger.error(f"Failed to create secure connection: {str(e)}")
        return None

def close_connection(sock: Optional[ssl.SSLSocket]) -> None:
    """
    Closes the SSL socket connection properly.
    
    Args:
        sock: The SSL socket to close, or None if no connection exists
    """
    if sock is not None:
        try:
            sock.close()
            logging.info("Socket connection closed successfully")
        except Exception as e:
            logging.error(f"Failed to close socket: {str(e)}")

# Example usage
if __name__ == "__main__":
    HOST = "example.com"
    PORT = 443
    CA_CERT = "/path/to/ca_cert.pem"
    
    secure_sock = create_secure_connection(HOST, PORT, CA_CERT)
    if secure_sock:
        try:
            # Perform operations with the secure connection
            pass
        finally:
            close_connection(secure_sock)