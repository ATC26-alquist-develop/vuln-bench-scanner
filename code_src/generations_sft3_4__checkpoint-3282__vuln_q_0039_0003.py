```python
import socket
import threading
import logging
from typing import Tuple
import ssl

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class SecureTCPServer:
    def __init__(self, host: str = '0.0.0.0', port: int = 8888, cert_file: str = None, key_file: str = None):
        """Initialize the secure TCP server with proper security controls."""
        self.host = host
        self.port = port
        self.cert_file = cert_file
        self.key_file = key_file
        self.socket = None
        self.running = False
        
        # Validate inputs
        if not isinstance(port, int) or not (0 <= port < 65536):
            raise ValueError("Port must be an integer between 0 and 65536")
        if not isinstance(host, str):
            raise ValueError("Host must be a string")
            
        # Validate SSL configuration
        if cert_file and key_file:
            if not isinstance(cert_file, str) or not isinstance(key_file, str):
                raise ValueError("Certificate and key files must be strings")
            if not cert_file or not key_file:
                raise ValueError("Both certificate and key files must be provided")
        
    def start(self):
        """Start the secure TCP server."""
        try:
            # Create a secure socket
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            
            # Wrap socket with SSL/TLS
            if self.cert_file and self.key_file:
                context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
                context.load_cert_chain(certfile=self.cert_file, keyfile=self.key_file)
                self.socket = context.wrap_socket(self.socket, server_side=True)
                
            # Bind to address and port
            self.socket.bind((self.host, self.port))
            self.socket.listen(5)
            self.running = True
            
            logging.info(f"Server started on {self.host}:{self.port}")
            
            while self.running:
                try:
                    client_socket, address = self.socket.accept()
                    client_thread = threading.Thread(target=self.handle_client, args=(client_socket, address))
                    client_thread.start()
                except ssl.SSLError as e:
                    logging.error(f"SSL Error: {e}")
                except Exception as e:
                    logging.error(f"Error accepting connection: {e}")
                    
        except Exception as e:
            logging.error(f"Error starting server: {e}")
            self.running = False
        finally:
            self.cleanup()
            
    def handle_client(self, client_socket: ssl.SSLSocket, address: Tuple[str, int]):
        """Handle individual client connections."""
        try:
            logging.info(f"New connection from {address}")
            while self.running:
                data = client_socket.recv(1024)
                if not data:
                    break
                # Process received data (implement your logic here)
                response = "Server received: " + data.decode('utf-8')
                client_socket.send(response.encode('utf-8'))
        except ssl.SSLError as e:
            logging.error(f"SSL Error with client {address}: {e}")
        except Exception as e:
            logging.error(f"Error handling client {address}: {e}")
        finally:
            client_socket.close()
            logging.info(f"Connection closed for {address}")

    def stop(self):
        """Safely stop the server."""
        self.running = False
        if self.socket:
            self.socket.close()
        self.cleanup()

    def cleanup(self):
        """Clean up resources."""
        if self.socket:
            self.socket.close()
        self.socket = None
        logging.info("Server stopped