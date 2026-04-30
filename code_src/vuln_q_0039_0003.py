import socket
import ssl
import logging
from typing import Tuple

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_secure_server(host: str = '0.0.0.0', port: int = 8443) -> None:
    """
    Create a secure TCP server using SSL/TLS.
    
    Args:
        host: Hostname or IP address to bind to (default: '0.0.0.0' - all interfaces)
        port: Port number to listen on (default: 8443)
    """
    # Validate inputs
    if not isinstance(host, str) or not isinstance(port, int):
        raise ValueError("Invalid input types")
    if not host:
        raise ValueError("Host cannot be empty")
    if not 1 <= port <= 65535:
        raise ValueError("Port must be between 1 and 65535")

    # Create a secure SSL context
    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    context.load_cert_chain(certfile="server.crt", keyfile="server.key")
    context.options |= ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1  # Disable older TLS versions

    # Create and bind the socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((host, port))
        sock.listen(5)
        logger.info(f"Server listening on {host}:{port}")

        while True:
            try:
                with context.wrap_socket(sock, server_side=True) as secure_sock:
                    conn, addr = secure_sock.accept()
                    logger.info(f"New connection from {addr}")
                    handle_client(conn, addr)
            except ssl.SSLError as e:
                logger.error(f"SSL error: {e}")
            except Exception as e:
                logger.error(f"Error handling connection: {e}")

def handle_client(conn: ssl.SSLSocket, addr: Tuple[str, int]) -> None:
    """
    Handle a client connection securely.
    
    Args:
        conn: SSL socket connection
        addr: Client address tuple (IP, port)
    """
    try:
        # Implement your secure client handling logic here
        # Example: Read data, process it, send response
        data = conn.recv(1024)
        if data:
            response = b"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n\r\nHello, secure world!"
            conn.sendall(response)
    except ssl.SSLError as e:
        logger.error(f"SSL error with {addr}: {e}")
    except Exception as e:
        logger.error(f"Error handling client {addr}: {e}")
    finally:
        conn.close()
        logger.info(f"Connection closed with {addr}")

if __name__ == "__main__":
    try:
        create_secure_server()
    except Exception as e:
        logger.critical(f"Server startup failed: {e}")