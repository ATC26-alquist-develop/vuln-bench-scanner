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
    """
    try:
        # Create a secure SSL context
        context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
        context.check_hostname = True
        context.verify_mode = ssl.CERT_REQUIRED
        
        # Create a socket and wrap it with SSL
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        ssl_sock = context.wrap_socket(sock, server_hostname=host)
        
        # Connect to the server
        ssl_sock.connect((host, port))
        
        # Log successful connection
        logging.info(f"Successfully connected to {host}:{port}")
        
        return ssl_sock
        
    except ssl.SSLError as e:
        logging.error(f"SSL error occurred: {str(e)}")
    except socket.error as e:
        logging.error(f"Socket error occurred: {str(e)}")
    except Exception as e:
        logging.error(f"Unexpected error occurred: {str(e)}")
        
    return None

def close_connection(ssl_sock: ssl.SSLSocket) -> None:
    """
    Closes the SSL socket connection.
    
    Args:
        ssl_sock (ssl.SSLSocket): The SSL socket to close
    """
    try:
        ssl_sock.close()
        logging.info("SSL socket connection closed")
    except Exception as e:
        logging.error(f"Error closing SSL socket: {str(e)}")

def main():
    host = "example.com"
    port = 443
    
    ssl_sock = create_secure_connection(host, port)
    if ssl_sock:
        try:
            # Perform operations with the SSL socket here
            pass
        finally:
            close_connection(ssl_sock)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()