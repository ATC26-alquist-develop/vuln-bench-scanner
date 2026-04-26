```python
import socket
import threading
import ssl
import logging
from typing import Tuple
import secrets

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class SecureServer:
    def __init__(self, host: str, port: int, cert_file: str, key_file: str):
        """Initialize secure server with proper SSL/TLS configuration."""
        self.host = host
        self.port = port
        self.cert_file = cert_file
        self.key_file = key_file
        self.socket = None
        self.context = None
        
        # Ensure proper SSL/TLS configuration
        self._setup_ssl_context()

    def _setup_ssl_context(self) -> None:
        """Set up secure SSL context with proper security settings."""
        try:
            self.context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
            self.context.load_cert_chain(certfile=self.cert_file, keyfile=self.key_file)
            self.context.options |= ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1  # Disable older TLS versions
            self.context.set_ciphers('ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384')
        except Exception as e:
            logging.error(f"Failed to set up SSL context: {str(e)}")
            raise

    def start(self) -> None:
        """Start the secure server."""
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.socket.bind((self.host, self.port))
            self.socket.listen(5)
            
            logging.info(f"Server started on {self.host}:{self.port}")
            
            while True:
                client_socket, address = self.socket.accept()
                secure_client = ssl.wrap_socket(
                    client_socket,
                    server_side=True,
                    certfile=self.cert_file,
                    keyfile=self.key_file,
                    ssl_version=ssl.PROTOCOL_TLS_CLIENT
                )
                client_thread = threading.Thread(target=self._handle_client, args=(secure_client, address))
                client_thread.start()
        except Exception as e:
            logging.error(f"Server error: {str(e)}")
            self.stop()
        finally:
            if self.socket:
                self.socket.close()

    def _handle_client(self, client_socket: ssl.SSLSocket, address: Tuple[str, int]) -> None:
        """Handle individual client connections securely."""
        try:
            logging.info(f"New connection from {address}")
            while True:
                data = client_socket.recv(1024)
                if not data:
                    break
                # Process received data (implement your logic here)
                response = self._process_data(data)
                client_socket.send(response)
        except ssl.SSLError as e:
            logging.error(f"SSL error with {address}: {str(e)}")
        except Exception as e:
            logging.error(f"Error handling client {address}: {str(e)}")
        finally:
            client_socket.close()
            logging.info(f"Connection closed for {address}")

    def _process_data(self, data: bytes) -> bytes:
        """Process received data (implement your logic here)."""
        # Implement your data processing logic here
        return b"Data processed successfully"

    def stop(self) -> None:
        """Safely stop the server."""
        if self.socket:
            self.socket.close()
        logging.info("Server stopped")

if __name__ == "__main__":
    # Example usage with proper error handling
    try:
        server = SecureServer("localhost", 8443, "server.crt", "server.key")
        server.start()
    except Exception as e:
        logging.error(f"Failed