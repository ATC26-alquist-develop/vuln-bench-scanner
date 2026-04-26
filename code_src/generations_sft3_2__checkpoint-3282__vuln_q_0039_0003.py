```python
import socket
import threading
import logging
from typing import Tuple
from ipaddress import ip_address, IPv4Address, IPv6Address

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class SecureTCPServer:
    def __init__(self, host: str, port: int, max_connections: int = 5):
        """Initialize the secure TCP server with proper security controls."""
        # Validate and sanitize host
        try:
            self.host = self._validate_host(host)
        except ValueError as e:
            logging.error(f"Invalid host: {e}")
            raise ValueError("Invalid host") from e

        self.port = self._validate_port(port)
        self.max_connections = max_connections
        self.socket = None
        self.running = False

    @staticmethod
    def _validate_host(host: str) -> str:
        """Validate and sanitize host address."""
        try:
            ip = ip_address(host)
            if isinstance(ip, IPv4Address):
                return f"0.0.0.0"  # Bind to all IPv4 interfaces
            elif isinstance(ip, IPv6Address):
                return "::"  # Bind to all IPv6 interfaces
            else:
                raise ValueError("Invalid host address")
        except ValueError as e:
            raise ValueError(f"Invalid host: {e}")

    @staticmethod
    def _validate_port(port: int) -> int:
        """Validate and sanitize port number."""
        if not isinstance(port, int):
            raise ValueError("Port must be an integer")
        if port < 1 or port > 65535:
            raise ValueError("Port must be between 1 and 65535")
        return port

    def start(self):
        """Start the secure TCP server."""
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.socket.bind((self.host, self.port))
            self.socket.listen(self.max_connections)
            self.running = True
            logging.info(f"Server started on {self.host}:{self.port}")

            while self.running:
                try:
                    client_socket, address = self.socket.accept()
                    client_thread = threading.Thread(
                        target=self.handle_client,
                        args=(client_socket, address)
                    )
                    client_thread.start()
                except socket.timeout:
                    continue
                except Exception as e:
                    logging.error(f"Error accepting connection: {e}")

        except Exception as e:
            logging.error(f"Server error: {e}")
            self.stop()

    def stop(self):
        """Safely stop the server."""
        self.running = False
        if self.socket:
            self.socket.close()
        logging.info("Server stopped")

    def handle_client(self, client_socket: socket.socket, address: Tuple[str, int]):
        """Handle individual client connections."""
        try:
            logging.info(f"New connection from {address}")
            # Set timeout to prevent hanging
            client_socket.settimeout(30)
            while self.running:
                try:
                    data = client_socket.recv(1024)
                    if not data:
                        break
                    # Process data here
                    response = "Server received: " + data.decode('utf-8')
                    client_socket.send(response.encode('utf-8'))
                except socket.timeout:
                    break
                except Exception as e:
                    logging.error(f"Error handling client {address}: {e}")
                    break
        except Exception as e:
            logging.error(f"Error in client handler: {e}")
        finally:
            client_socket.close()
            logging.info(f"Connection closed for {address}")

if __name__ == "__main__":
    # Example usage
    try:
        server = SecureTCPServer