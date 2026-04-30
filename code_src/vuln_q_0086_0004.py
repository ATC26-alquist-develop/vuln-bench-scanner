```python
import socket
import ssl
import logging
from typing import Tuple
from pathlib import Path

def setup_logging():
    """Set up secure logging configuration."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('server.log'),
            logging.StreamHandler()
        ]
    )

def validate_port(port: int) -> None:
    """Validate that the port is within the valid range."""
    if not (1024 <= port <= 65535):
        raise ValueError("Port must be between 1024 and 65535")

def create_secure_context() -> ssl.SSLContext:
    """Create a secure SSL context with strong settings."""
    context = ssl.create_default_context(
        purpose=ssl.Purpose.CLIENT_AUTH,
        cafile=None  # Use system's default CA cert
    )
    
    # Require strong cipher suites
    context.set_ciphers('HIGH:!aNULL:!MD5:!RC4')
    
    # Require minimum TLS version
    context.minimum_version = ssl.TLSVersion.TLSv1_2
    
    return context

def start_server(host: str = '127.0.0.1', port: int = 8443) -> None:
    """
    Start a secure HTTPS server on localhost by default.
    Change host and port for production use.
    """
    try:
        # Validate inputs
        if not isinstance(host, str) or not isinstance(port, int):
            raise ValueError("Invalid host or port type")
        
        validate_port(port)
        
        # Create secure context
        context = create_secure_context()
        
        # Create and bind socket with proper error handling
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.setsockopt(
                socket.SOL_SOCKET,
                socket.SO_REUSEADDR,
                1
            )
            
            try:
                server_socket.bind((host, port))
                server_socket.listen(5)
                logging.info(f"Server started on {host}:{port}")
                
                while True:
                    try:
                        client_socket, addr = server_socket.accept()
                        with context.wrap_socket(
                            client_socket,
                            server_side=True,
                            do_handshake_on_connect=True
                        ) as secure_client:
                            logging.info(f"Secure connection from {addr}")
                            data = secure_client.recv(1024).decode('utf-8')
                            logging.info(f"Received: {data}")
                            response = "Hello, secure world!"
                            secure_client.send(response.encode('utf-8'))
                    except ssl.SSLCertVerificationError as e:
                        logging.error(f"SSL certificate verification failed: {e}")
                    except Exception as e:
                        logging.error(f"Error handling client: {e}")
            except socket.error as e:
                logging.error(f"Socket error: {e}")
            finally:
                logging.info("Server shutting down")
    
    except Exception as e:
        logging.error(f"Server initialization failed: {e}")

if __name__ == "__main__":
    setup_logging()
    start_server()
```