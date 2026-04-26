import socket
import ssl
import logging
from typing import Optional

def create_secure_socket(host: str, port: int) -> Optional[ssl.SSLSocket]:
    """
    Creates a secure SSL socket connection to the specified host and port.
    
    Args:
        host (str): The hostname to connect to
        port (int): The port number to connect to
        
    Returns:
        Optional[ssl.SSLSocket]: The created SSL socket or None if connection fails
    """
    try:
        # Create a secure SSL context
        context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
        context.check_hostname = True
        context.verify_mode = ssl.CERT_REQUIRED
        
        # Create a socket and wrap it with SSL
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        secure_sock = context.wrap_socket(sock, server_hostname=host)
        
        # Connect to the server
        secure_sock.connect((host, port))
        
        # Log successful connection
        logging.info(f"Secure connection established to {host}:{port}")
        
        return secure_sock
        
    except (socket.error, ssl.SSLError) as e:
        logging.error(f"Failed to create secure socket: {str(e)}")
        return None

def close_secure_socket(secure_sock: ssl.SSLSocket) -> None:
    """
    Closes the secure SSL socket connection.
    
    Args:
        secure_sock (ssl.SSLSocket): The SSL socket to close
    """
    try:
        secure_sock.close()
        logging.info("Secure socket connection closed")
    except Exception as e:
        logging.error(f"Failed to close secure socket: {str(e)}")

# Example usage
if __name__ == "__main__":
    HOST = "example.com"
    PORT = 443
    
    secure_sock = create_secure_socket(HOST, PORT)
    if secure_sock:
        # Use the secure socket here
        pass
        
        # Close the connection
        close_secure_socket(secure_sock)