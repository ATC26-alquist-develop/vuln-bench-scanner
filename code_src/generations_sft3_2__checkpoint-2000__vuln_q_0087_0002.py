```python
import socket
import ssl
import secrets
import logging
from typing import Tuple
from dataclasses import dataclass

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class ServerConfig:
    host: str = 'localhost'
    port: int = 8443
    cert_file: str = 'server.crt'
    key_file: str = 'server.key'
    max_connections: int = 5
    buffer_size: int = 1024

class SecureServer:
    def __init__(self, config: ServerConfig):
        self.config = config
        self.socket = None
        self.context = None
        
    def setup_ssl_context(self) -> None:
        """Set up secure SSL context with strong security settings"""
        try:
            # Create SSL context with secure defaults
            self.context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
            self.context.options |= ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1  # Disable older TLS versions
            self.context.set_ciphers('ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384')
            self.context.options |= ssl.OP_NO_COMPRESSION  # Disable compression
            self.context.verify_mode = ssl.CERT_REQUIRED
            self.context.load_cert_chain(certfile=self.config.cert_file, keyfile=self.config.key_file)
        except Exception as e:
            logger.error(f"SSL context setup failed: {e}")
            raise

    def start_server(self) -> None:
        """Start the secure server"""
        try:
            # Create socket
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            
            # Bind socket
            self.socket.bind((self.config.host, self.config.port))
            self.socket.listen(self.config.max_connections)
            
            # Setup SSL context
            self.setup_ssl_context()
            
            logger.info(f"Server started on {self.config.host}:{self.config.port}")
            
            while True:
                client_socket, address = self.socket.accept()
                secure_client = self.context.wrap_socket(client_socket, server_side=True)
                logger.info(f"New connection from {address}")
                self.handle_client(secure_client, address)
                
        except Exception as e:
            logger.error(f"Server error: {e}")
            self.close_connections()
        finally:
            if self.socket:
                self.socket.close()

    def handle_client(self, client_socket: ssl.SSLSocket, address: Tuple[str, int]) -> None:
        """Handle client connection securely"""
        try:
            while True:
                data = client_socket.recv(self.config.buffer_size)
                if not data:
                    break
                # Process received data (implement your logic here)
                response = "Received: " + data.decode('utf-8')
                client_socket.send(response.encode('utf-8'))
        except ssl.SSLError as e:
            logger.error(f"SSL error with {address}: {e}")
        except Exception as e:
            logger.error(f"Error handling client {address}: {e}")
        finally:
            client_socket.close()
            logger.info(f"Connection closed for {address}")

    def close_connections(self) -> None:
        """Safely close all connections"""
        if self.socket:
            self.socket.close()
        logger.info("Server shutdown complete")

def main() -> None:
    """Main function to set up and run the server"""
    try:
        # Generate secure random port number
        config = ServerConfig(port=secrets.randbelow(65535) + 1024)
        server = SecureServer(config)
        server.start_server()
    except Exception as e: