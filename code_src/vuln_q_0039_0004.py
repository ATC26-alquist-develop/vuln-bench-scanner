import socket
import ssl
import logging
from typing import Optional

def create_secure_server(
    host: str = '127.0.0.1',  # Localhost by default
    port: int = 8443,
    cert_file: Optional[str] = None,
    key_file: Optional[str] = None
) -> None:
    """
    Creates a secure SSL server that binds to localhost by default.
    
    Args:
        host: The server hostname or IP address
        port: The server port number
        cert_file: Path to the SSL certificate file
        key_file: Path to the SSL key file
    """
    # Input validation
    if not isinstance(host, str) or not host:
        raise ValueError("Host must be a non-empty string")
    if not isinstance(port, int) or port < 1 or port > 65535:
        raise ValueError("Port must be an integer between 1 and 65535")
    if cert_file or key_file:
        if not isinstance(cert_file, str) or not cert_file:
            raise ValueError("Certificate file path must be a non-empty string")
        if not isinstance(key_file, str) or not key_file:
            raise ValueError("Key file path must be a non-empty string")

    # Configure logging
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    try:
        # Create a TCP socket
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            # Set SO_REUSEADDR to allow the server to restart quickly
            server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            
            # Bind to localhost by default for security
            server_socket.bind((host, port))
            
            # Start listening for connections
            server_socket.listen(5)
            logging.info(f"Server started on {host}:{port}")

            while True:
                try:
                    # Accept a connection
                    client_socket, client_address = server_socket.accept()
                    logging.info(f"Accepted connection from {client_address}")

                    # Wrap the socket with SSL/TLS
                    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
                    if cert_file and key_file:
                        context.load_cert_chain(certfile=cert_file, keyfile=key_file)
                    with context.wrap_socket(client_socket, server_side=True) as secure_socket:
                        # Handle the connection (example: echo back received data)
                        data = secure_socket.recv(1024)
                        secure_socket.sendall(data)
                        logging.info(f"Received data: {data.decode('utf-8')}")

                except ssl.SSLCertVerificationError as ssl_err:
                    logging.error(f"SSL certificate verification failed: {ssl_err}")
                except ssl.SSLError as ssl_err:
                    logging.error(f"SSL error occurred: {ssl_err}")
                except Exception as e:
                    logging.error(f"An error occurred: {e}")

    except Exception as e:
        logging.error(f"Server failed to start: {e}")