import socket
import ssl
import logging
from typing import Tuple

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_secure_context() -> ssl.SSLContext:
    """Create a secure SSL context with strong security settings."""
    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    context.options |= ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1  # Disable older TLS versions
    context.set_ciphers('ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384')
    return context

def secure_server(host: str, port: int) -> None:
    """Run a secure server that listens for incoming connections."""
    context = create_secure_context()
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            server_socket.bind((host, port))
            server_socket.listen(1)
            logger.info(f"Server listening on {host}:{port}")
            
            while True:
                try:
                    client_socket, addr = server_socket.accept()
                    with context.wrap_socket(client_socket, server_side=True) as secure_client:
                        logger.info(f"Secure connection from {addr}")
                        secure_client.sendall(b"Hello, secure client!")
                except ssl.SSLError as e:
                    logger.error(f"SSL error: {e}")
                except Exception as e:
                    logger.error(f"Error handling client: {e}")
        except Exception as e:
            logger.error(f"Server error: {e}")

def secure_client(host: str, port: int) -> None:
    """Run a secure client that connects to the server."""
    context = create_secure_context()
    
    with socket.create_connection((host, port)) as sock:
        with context.wrap_socket(sock, server_hostname=host) as secure_sock:
            logger.info("Connected to server securely")
            data = secure_sock.recv(1024)
            logger.info(f"Received: {data.decode('utf-8')}")

if __name__ == "__main__":
    # Example usage - run in separate processes
    # secure_server('localhost', 8443)
    # secure_client('localhost', 8443)