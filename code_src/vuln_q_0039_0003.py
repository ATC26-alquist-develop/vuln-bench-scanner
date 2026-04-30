import socket
import ssl
import logging
from typing import Tuple
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename=Path('server.log')
)

class SecureTCPServer:
    def __init__(self, host: str = '127.0.0.1', port: int = 8443):
        """
        Initialize the secure TCP server with default values.
        
        :param host: Localhost by default for security
        :param port: Using HTTPS port 8443
        """
        self.host = host
        self.port = port
        self.context = None

    def _create_context(self) -> None:
        """Create SSL context with strong security settings."""
        try:
            # Create context with TLS 1.3 and strong cipher suites
            self.context = ssl.create_default_context(
                purpose=ssl.Purpose.CLIENT_AUTH,
                cafile=None  # Use system's root certificates
            )
            # Force TLS 1.3
            self.context.minimum_version = ssl.TLSVersion.TLSv1_3
        except ssl.SSLCertVerificationError as e:
            logging.error(f"SSL context creation failed: {e}")
            raise

    def _validate_client(self, client_address: Tuple[str, int]) -> None:
        """Validate client address to prevent potential attacks."""
        if not client_address[0].isalnum() or not client_address[1].isdigit():
            raise ValueError("Invalid client address format")

    def start(self) -> None:
        """Start the secure TCP server."""
        try:
            # Validate inputs
            if not isinstance(self.host, str) or not isinstance(self.port, int):
                raise ValueError("Invalid host or port type")

            # Create SSL context
            self._create_context()

            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
                # Bind to localhost by default for security
                server_socket.bind((self.host, self.port))
                server_socket.listen(5)
                logging.info(f"Server started on {self.host}:{self.port}")

                while True:
                    try:
                        client_socket, client_address = server_socket.accept()
                        logging.info(f"New connection from {client_address}")

                        # Validate client address
                        self._validate_client(client_address)

                        # Wrap socket with SSL
                        with self.context.wrap_socket(
                            client_socket,
                            server_side=True
                        ) as secure_socket:
                            try:
                                # Handle client (example: echo message)
                                data = secure_socket.recv(1024).decode('utf-8')
                                logging.info(f"Received: {data}")
                                response = f"Server received: {data}"
                                secure_socket.send(response.encode('utf-8'))
                            except ssl.SSLCertVerificationError as e:
                                logging.error(f"SSL certificate verification failed: {e}")
                            except Exception as e:
                                logging.error(f"Error handling client: {e}")
                            finally:
                                secure_socket.close()

                    except Exception as e:
                        logging.error(f"Error accepting connection: {e}")

        except Exception as e:
            logging.error(f"Server startup failed: {e}")
            raise

if __name__ == "__main__":
    try:
        server = SecureTCPServer()
        server.start()
    except Exception as e:
        logging.critical(f"Critical error: {e}")