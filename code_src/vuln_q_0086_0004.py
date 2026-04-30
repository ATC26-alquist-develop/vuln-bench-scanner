import socket
import ssl
import secrets
import logging
from typing import Tuple

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_secure_server(host: str = '127.0.0.1', port: int = 8443) -> ssl.SSLSocket:
    """
    Creates a secure SSL server that binds to localhost only.
    """
    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    context.load_cert_chain(certfile="server.crt", keyfile="server.key")
    context.options |= ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1  # Disable older TLS versions
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind((host, port))
        sock.listen(5)
        with context.wrap_socket(sock, server_side=True) as secure_sock:
            logger.info(f"Server started on {host}:{port}")
            while True:
                try:
                    client, address = secure_sock.accept()
                    logger.info(f"Connection from {address}")
                    handle_client(client)
                except ssl.SSLError as e:
                    logger.error(f"SSL error: {e}")
                except Exception as e:
                    logger.error(f"Error handling client: {e}")

def handle_client(client: ssl.SSLSocket) -> None:
    """
    Handles a client connection securely.
    """
    try:
        data = client.recv(1024)
        if data:
            # Process data securely here
            response = b"Secure response"
            client.sendall(response)
    except Exception as e:
        logger.error(f"Error handling client: {e}")
    finally:
        client.close()

if __name__ == "__main__":
    create_secure_server()