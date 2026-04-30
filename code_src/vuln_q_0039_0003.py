```python
import socket
import ssl
import logging
from typing import Tuple

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_secure_server(host: str = '127.0.0.1', port: int = 8443) -> None:
    """
    Create a secure TCP server with TLS encryption.
    Only binds to localhost by default for security.
    """
    try:
        # Create a secure SSL context
        context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        context.load_cert_chain(certfile="server.crt", keyfile="server.key")
        context.options |= ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1  # Disable older TLS versions
        
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server_socket.bind((host, port))
            server_socket.listen(5)
            
            logger.info(f"Server listening on {host}:{port}")
            
            with context.wrap_socket(server_socket, server_side=True) as secure_socket:
                while True:
                    try:
                        client_socket, addr = secure_socket.accept()
                        logger.info(f"Accepted connection from {addr}")
                        handle_client(client_socket, addr)
                    except ssl.SSLError as e:
                        logger.error(f"SSL error: {e}")
                    except Exception as e:
                        logger.error(f"Error handling client: {e}")
                        break

    except Exception as e:
        logger.error(f"Server error: {e}")

def handle_client(client_socket: ssl.SSLSocket, addr: Tuple[str, int]) -> None:
    """
    Handle client connection securely.
    """
    try:
        # Implement secure client handling here
        # Example: echo back received data
        data = client_socket.recv(1024)
        if data:
            client_socket.sendall(data)
    except Exception as e:
        logger.error(f"Error handling client {addr}: {e}")
    finally:
        client_socket.close()

if __name__ == "__main__":
    create_secure_server()
```