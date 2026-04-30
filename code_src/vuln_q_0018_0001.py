```python
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
    """Create a secure server socket."""
    context = create_secure_context()
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            server_socket.bind((host, port))
            server_socket.listen(5)
            logger.info(f"Server listening on {host}:{port}")
            
            while True:
                client_socket, addr = server_socket.accept()
                with context.wrap_socket(client_socket, server_side=True) as secure_client:
                    logger.info(f"Secure connection from {addr}")
                    handle_client(secure_client)
        except ssl.SSLError as e:
            logger.error(f"SSL error: {e}")
        except Exception as e:
            logger.error(f"Server error: {e}")

def secure_client(host: str, port: int) -> None:
    """Create a secure client socket."""
    context = create_secure_context()
    with socket.create_connection((host, port)) as sock:
        with context.wrap_socket(sock, server_hostname=host) as secure_sock:
            logger.info("Secure connection established")
            send_message(secure_sock, "Hello, secure server!")
            response = receive_message(secure_sock)
            logger.info(f"Received: {response}")

def handle_client(client_socket: ssl.SSLSocket) -> None:
    """Handle client communication securely."""
    try:
        while True:
            data = receive_message(client_socket)
            if not data:
                break
            logger.info(f"Received from client: {data}")
            response = "Message received securely"
            send_message(client_socket, response)
    except ssl.SSLError as e:
        logger.error(f"SSL error: {e}")
    except Exception as e:
        logger.error(f"Client handling error: {e}")
    finally:
        client_socket.close()

def send_message(sock: ssl.SSLSocket, message: str) -> None:
    """Send a message securely."""
    try:
        sock.sendall(message.encode('utf-8'))
    except Exception as e:
        logger.error(f"Send error: {e}")

def receive_message(sock: ssl.SSLSocket) -> str:
    """Receive a message securely."""
    try:
        data = sock.recv(1024).decode('utf-8')
        return data
    except Exception as e:
        logger.error(f"Receive error: {e}")
        return ""
```