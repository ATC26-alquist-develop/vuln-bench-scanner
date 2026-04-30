import socket
import ssl
import logging
from typing import Tuple

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_secure_server(host: str = '127.0.0.1', port: int = 8443) -> ssl.SSLSocket:
    """Create a secure SSL server that only accepts connections from localhost."""
    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    context.load_cert_chain(certfile="server.crt", keyfile="server.key")
    context.options |= ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1  # Disable older TLS versions
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind((host, port))
        sock.listen(5)
        logger.info(f"Server listening on {host}:{port}")
        
        while True:
            try:
                client_socket, addr = sock.accept()
                with context.wrap_socket(client_socket, server_side=True) as secure_socket:
                    logger.info(f"Secure connection from {addr}")
                    secure_socket.sendall(b"Hello, secure client!")
                    secure_socket.close()
            except ssl.SSLError as e:
                logger.error(f"SSL error: {e}")
            except Exception as e:
                logger.error(f"Error accepting connection: {e}")

if __name__ == "__main__":
    create_secure_server()