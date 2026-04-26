```python
import socket
import ssl
import secrets
import logging
from typing import Tuple

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SecureClientServer:
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
        self.context = self._create_ssl_context()
        
    def _create_ssl_context(self) -> ssl.SSLContext:
        """Create a secure SSL context with strong security settings."""
        context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
        context.options |= ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1  # Disable older TLS versions
        context.set_ciphers('ECDHE+AESGCM:ECDHE+CHACHA20:DHE+AESGCM:DHE+CHACHA20')
        context.check_hostname = True
        context.verify_mode = ssl.CERT_REQUIRED
        return context

    def _create_secure_socket(self) -> ssl.SSLSocket:
        """Create a secure socket with proper error handling."""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            ssl_sock = self.context.wrap_socket(sock, server_hostname=self.host)
            ssl_sock.settimeout(10)  # Set reasonable timeout
            return ssl_sock
        except (socket.error, ssl.SSLError) as e:
            logger.error(f"Failed to create secure socket: {e}")
            raise

    def start_server(self) -> None:
        """Start a secure server."""
        try:
            with self._create_secure_socket() as server_socket:
                server_socket.bind((self.host, self.port))
                server_socket.listen(5)
                logger.info(f"Server listening on {self.host}:{self.port}")
                
                while True:
                    client_socket, addr = server_socket.accept()
                    logger.info(f"Accepted connection from {addr}")
                    self._handle_client(client_socket)
        except Exception as e:
            logger.error(f"Server error: {e}")
            raise

    def _handle_client(self, client_socket: ssl.SSLSocket) -> None:
        """Handle client connections securely."""
        try:
            while True:
                data = client_socket.recv(1024)
                if not data:
                    break
                
                # Process received data (implement your logic here)
                response = self._process_data(data)
                
                # Send response
                client_socket.sendall(response)
        except ssl.SSLError as e:
            logger.error(f"SSL error with client: {e}")
        except Exception as e:
            logger.error(f"Error handling client: {e}")
        finally:
            client_socket.close()

    def _process_data(self, data: bytes) -> bytes:
        """Process received data (implement your logic here)."""
        # Implement your data processing logic
        # This is a placeholder implementation
        return b"Data processed successfully"

    def start_client(self, server_host: str, server_port: int) -> None:
        """Start a secure client."""
        try:
            with self._create_secure_socket() as client_socket:
                client_socket.connect((server_host, server_port))
                logger.info(f"Connected to {server_host}:{server_port}")
                
                # Send data
                message = b"Hello, server!"
                client_socket.sendall(message)
                
                # Receive response
                response = client_socket.recv(1024)
                logger.info(f"Received response: {response.decode()}")
        except ssl.SSLError as e:
            logger.error(f"SSL error with client: {e}")
        except Exception as e:
            logger.error(f"Error in client: {e}")
        finally:
            client_socket.close()

if __name__ == "__main__":
    # Example usage
    server = SecureClientServer