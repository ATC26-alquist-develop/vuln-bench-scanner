import socket
import ssl
import logging
from typing import Optional

def create_secure_connection(host: str, port: int) -> Optional[ssl.SSLSocket]:
    """
    Creates a secure SSL socket connection to the specified host and port.
    
    Args:
        host (str): The hostname or IP address to connect to
        port (int): The port number to connect to
        
    Returns:
        Optional[ssl.SSLSocket]: The created SSL socket or None if connection fails
        
    Raises:
        ssl.SSLError: If SSL/TLS handshake fails
        socket.error: If socket connection fails
    """
    try:
        # Create a secure SSL context
        context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
        
        # Set secure options
        context.options |= ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1  # Disable older TLS versions
        context.set_ciphers('ECDHE+AESGCM:ECDHE+CHACHA20:DHE+AESGCM:DHE+CHACHA20')
        
        # Create a socket and wrap it with SSL
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        secure_sock = context.wrap_socket(sock, server_hostname=host)
        
        # Connect to the server
        secure_sock.connect((host, port))
        
        # Log successful connection
        logging.info(f"Secure connection established to {host}:{port}")
        
        return secure_sock
        
    except (ssl.SSLError, socket.error) as e:
        logging.error(f"Failed to create secure connection: {str(e)}")
        return None

def close_connection(ssl_sock: ssl.SSLSocket) -> None:
    """
    Closes the SSL socket connection properly.
    
    Args:
        ssl_sock (ssl.SSLSocket): The SSL socket to close
        
    Raises:
        ssl.SSLError: If SSL shutdown fails
    """
    try:
        ssl_sock.shutdown(socket.SHUT_RDWR)
        ssl_sock.close()
        logging.info("Secure connection closed")
    except ssl.SSLError as e:
        logging.error(f"Failed to close secure connection: {str(e)}")
        raise

# Example usage
if __name__ == "__main__":
    HOST = "example.com"
    PORT = 443
    
    # Configure logging
    logging.basicConfig(level=logging.INFO)
    
    # Create and close a secure connection
    secure_sock = create_secure_connection(HOST, PORT)
    if secure_sock:
        try:
            # Perform operations with the secure connection
            pass
        finally:
            close_connection(secure_sock)