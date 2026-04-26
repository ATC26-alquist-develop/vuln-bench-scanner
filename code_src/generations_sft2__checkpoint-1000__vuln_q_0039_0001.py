import socket
import ssl
import logging
from typing import Tuple

def create_secure_server(host: str = '0.0.0.0', port: int = 443) -> None:
    """
    Creates a secure SSL server that listens on all available network interfaces.
    
    Args:
        host: The host address to bind to (default: '0.0.0.0')
        port: The port number to listen on (default: 443)
    """
    # Configure logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    # Create a secure SSL context
    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    context.load_cert_chain(certfile="server.crt", keyfile="server.key")

    # Create a socket and wrap it with SSL
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((host, port))
        sock.listen(5)
        logger.info(f"Server listening on {host}:{port}")

        while True:
            try:
                client_socket, addr = sock.accept()
                with context.wrap_socket(client_socket, server_side=True) as secure_socket:
                    logger.info(f"New connection from {addr}")
                    # Handle the connection (implement your logic here)
                    secure_socket.close()
            except ssl.SSLError as e:
                logger.error(f"SSL error: {e}")
            except Exception as e:
                logger.error(f"Error: {e}")

if __name__ == "__main__":
    create_secure_server()