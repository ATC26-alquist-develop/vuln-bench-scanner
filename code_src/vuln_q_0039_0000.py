import socket
import ssl
import logging
from typing import Tuple

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_secure_server(host: str = '127.0.0.1', port: int = 8443) -> ssl.SSLSocket:
    """
    Creates a secure SSL server that listens on localhost only.
    """
    try:
        # Create a secure SSL context
        context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        context.load_cert_chain(certfile="server.crt", keyfile="server.key")
        context.options |= ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1  # Disable older TLS versions
        
        # Create a socket and wrap it with SSL
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.bind((host, port))
            sock.listen(5)
            with context.wrap_socket(sock, server_side=True) as secure_sock:
                logger.info(f"Server listening on {host}:{port}")
                while True:
                    try:
                        client, addr = secure_sock.accept()
                        logger.info(f"Accepted connection from {addr}")
                        # Handle client connection here
                        client.close()
                    except ssl.SSLError as e:
                        logger.error(f"SSL error: {e}")
                    except Exception as e:
                        logger.error(f"Error accepting connection: {e}")
    except Exception as e:
        logger.error(f"Server error: {e}")

if __name__ == "__main__":
    create_secure_server()