```python
import socket
import threading
import logging
from typing import Tuple
from ipaddress import ip_address, IPv4Address, IPv6Address
import ssl

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class SecureTCPServer:
    def __init__(self, host: str, port: int, cert_file: str, key_file: str):
        """Initialize the secure TCP server with proper security controls."""
        # Validate host
        try:
            self.host = self._validate_host(host)
        except ValueError as e:
            logging.error(f"Invalid host: {e}")
            raise

        # Validate port
        if not (1024 <= port <= 65535):
            raise ValueError("Port must be between 1024 and 65535")
        
        self.port = port

        # Validate certificate and key files
        if not (cert_file and key_file):
            raise ValueError("Certificate and key files must be provided")
        
        self.cert_file = cert_file
        self.key_file = key_file

        # Create SSL context
        self.ssl_context = self._create_ssl_context()

        # Thread-safe lock for connection handling
        self.lock = threading.Lock()

    @staticmethod
    def _validate_host(host: str) -> str:
        """Validate host address."""
        try:
            ip = ip_address(host)
            if isinstance(ip, IPv4Address):
                return f"0.0.0.0"  # Listen on all IPv4 interfaces
            elif isinstance(ip, IPv6Address):
                return f"[::]"  # Listen on all IPv6 interfaces
            else:
                raise ValueError("Invalid host address")
        except ValueError as e:
            raise ValueError(f"Invalid host: {e}")

    @staticmethod
    def _create_ssl_context() -> ssl.SSLContext:
        """Create a secure SSL context."""
        context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        context.load_cert_chain(certfile=SecureTCPServer.cert_file, 
                              keyfile=SecureTCPServer.key_file)
        context.options |= ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1  # Disable older TLS versions
        context.set_ciphers('ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384')
        return context

    def start(self) -> None:
        """Start the secure TCP server."""
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
                server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                server_socket.bind((self.host, self.port))
                server_socket.listen(5)
                logging.info(f"Server listening on {self.host}:{self.port}")

                with self.ssl_context.wrap_socket(server_socket, server_side=True) as secure_socket:
                    while True:
                        try:
                            client_socket, address = secure_socket.accept()
                            client_thread = threading.Thread(
                                target=self._handle_client,
                                args=(client_socket, address),
                                daemon=True
                            )
                            client_thread.start()
                        except ssl.SSLError as e:
                            logging.error(f"SSL error: {e}")
                        except Exception as e:
                            logging.error(f"Error accepting connection: {e}")

        except Exception as e:
            logging.error(f"Server error: {e}")
            raise

    def _handle_client(self, client_socket: ssl.SSLSocket, address: Tuple[str, int]) -> None:
        """Handle client connections securely."""
        try:
            with self.lock:
                logging.info(f"New connection from {address}")
                client_socket.sendall(b"Connection successful