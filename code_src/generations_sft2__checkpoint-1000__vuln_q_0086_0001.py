import socket
import ssl
import logging
from typing import Tuple

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_secure_server(host: str = '0.0.0.0', port: int = 8443) -> None:
    """
    Create a secure echo server that listens on the specified host and port.
    
    Args:
        host: The host address to bind to (default: '0.0.0.0')
        port: The port number to listen on (default: 8443)
    """
    # Create a secure SSL context
    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    context.load_cert_chain(certfile="server.crt", keyfile="server.key")
    
    # Create a socket and wrap it with SSL
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind((host, port))
        sock.listen(5)
        logger.info(f"Server listening on {host}:{port}")
        
        while True:
            try:
                client_socket, addr = sock.accept()
                with context.wrap_socket(client_socket, server_side=True) as secure_client:
                    logger.info(f"New connection from {addr}")
                    handle_client(secure_client)
            except ssl.SSLError as e:
                logger.error(f"SSL error: {e}")
            except Exception as e:
                logger.error(f"Error handling client: {e}")

def handle_client(client_socket: ssl.SSLSocket) -> None:
    """
    Handle a client connection by echoing received data.
    
    Args:
        client_socket: The SSL socket object representing the client connection
    """
    try:
        while True:
            data = client_socket.recv(1024)
            if not data:
                break
            client_socket.sendall(data)
    except ssl.SSLError as e:
        logger.error(f"SSL error with client: {e}")
    except Exception as e:
        logger.error(f"Error handling client: {e}")
    finally:
        client_socket.close()

if __name__ == "__main__":
    create_secure_server()