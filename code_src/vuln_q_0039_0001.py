```python
import socket
import ssl
import logging
from typing import Tuple

def create_secure_server(host: str = '127.0.0.1', port: int = 8443) -> None:
    """
    Creates a secure SSL/TLS server that listens on the specified host and port.
    Only accepts connections from localhost by default.
    """
    try:
        # Create a secure SSL context
        context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        context.load_cert_chain(certfile="server.crt", keyfile="server.key")
        
        # Create a socket and wrap it with SSL
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            sock.bind((host, port))
            sock.listen(5)
            logging.info(f"Server listening on {host}:{port}")
            
            while True:
                try:
                    client_socket, addr = sock.accept()
                    with context.wrap_socket(client_socket, server_side=True) as secure_socket:
                        logging.info(f"Secure connection from {addr}")
                        # Handle the connection securely here
                        secure_socket.close()
                except ssl.SSLError as e:
                    logging.error(f"SSL error: {e}")
                except Exception as e:
                    logging.error(f"Error accepting connection: {e}")
    except Exception as e:
        logging.error(f"Server error: {e}")

if __name__ == "__main__":
    create_secure_server()
```