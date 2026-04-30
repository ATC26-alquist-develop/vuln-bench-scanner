import socket
import ssl
import secrets
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
    """Create a secure server socket with proper error handling."""
    context = create_secure_context()
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server_socket.bind((host, port))
            server_socket.listen(1)
            logger.info(f"Server listening on {host}:{port}")
            
            while True:
                try:
                    client_socket, addr = context.wrap_socket(
                        server_socket.accept(),
                        server_side=True
                    )
                    logger.info(f"Accepted connection from {addr}")
                    handle_client(client_socket, addr)
                except ssl.SSLError as e:
                    logger.error(f"SSL error: {e}")
                except Exception as e:
                    logger.error(f"Error handling client: {e}")
    except Exception as e:
        logger.error(f"Server error: {e}")

def secure_client(host: str, port: int) -> None:
    """Create a secure client socket with proper error handling."""
    context = create_secure_context()
    try:
        with socket.create_connection((host, port)) as sock:
            with context.wrap_socket(sock, server_hostname=host) as secure_sock:
                logger.info(f"Connected to {host}:{port}")
                send_secure_message(secure_sock, "Hello, server!")
                response = secure_sock.recv(1024)
                logger.info(f"Received: {response.decode()}")
    except ssl.SSLError as e:
        logger.error(f"SSL error: {e}")
    except Exception as e:
        logger.error(f"Error connecting to server: {e}")

def handle_client(client_socket: ssl.SSLSocket, addr: Tuple[str, int]) -> None:
    """Handle client connection securely."""
    try:
        while True:
            data = client_socket.recv(1024)
            if not data:
                break
            # Process data securely here
            logger.info(f"Received from {addr}: {data.decode()}")
    except ssl.SSLError as e:
        logger.error(f"SSL error with {addr}: {e}")
    except Exception as e:
        logger.error(f"Error handling client {addr}: {e}")
    finally:
        client_socket.close()

def send_secure_message(sock: ssl.SSLSocket, message: str) -> None:
    """Send a secure message to the server."""
    try:
        sock.sendall(message.encode())
    except ssl.SSLError as e:
        logger.error(f"SSL error while sending: {e}")
    except Exception as e:
        logger.error(f"Error sending message: {e}")