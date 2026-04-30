```python
import socket
import logging
from typing import Tuple

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("server.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def handle_client(client_socket: socket.socket, client_address: Tuple[str, int]) -> None:
    """
    Handles communication with a connected client.
    
    Args:
        client_socket: The socket object for the client connection.
        client_address: A tuple containing the client's IP address and port.
    """
    try:
        logger.info(f"Accepted connection from {client_address[0]}:{client_address[1]}")
        
        while True:
            data = client_socket.recv(1024)
            if not data:
                break
            client_socket.sendall(data)
        
    except Exception as e:
        logger.error(f"Error handling client {client_address}: {str(e)}")
    finally:
        client_socket.close()
        logger.info(f"Closed connection from {client_address[0]}:{client_address[1]}")

def run_server(host: str = '127.0.0.1', port: int = 8888) -> None:
    """
    Runs the echo server.
    
    Args:
        host: The IP address to bind the server to (default '127.0.0.1').
        port: The port number to bind the server to (default 8888).
    """
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server_socket.bind((host, port))
            server_socket.listen(5)
            logger.info(f"Server started on {host}:{port}")
            
            while True:
                try:
                    client_socket, client_address = server_socket.accept()
                    handle_client(client_socket, client_address)
                except Exception as e:
                    logger.error(f"Error accepting connection: {str(e)}")
    
    except Exception as e:
        logger.error(f"Server error: {str(e)}")

if __name__ == "__main__":
    run_server()
```