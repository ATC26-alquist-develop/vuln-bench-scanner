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
        """Initialize the secure TCP server with TLS encryption"""
        self.host = host
        self.port = port
        self.cert_file = cert_file
        self.key_file = key_file
        self.socket = None
        self.running = False
        
        # Validate inputs
        if not isinstance(port, int) or not 1 <= port <= 65535:
            raise ValueError("Port must be an integer between 1 and 65535")
        
        if not isinstance(host, str):
            raise ValueError("Host must be a string")
            
        if cert_file and not isinstance(cert_file, str):
            raise ValueError("Certificate file must be a string")
            
        if key_file and not isinstance(key_file, str):
            raise ValueError("Key file must be a string")

    def start(self):
        """Start the secure TCP server"""
        try:
            # Create SSL context
            context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
            if self.cert_file and self.key_file:
                context.load_cert_chain(certfile=self.cert_file, keyfile=self.key_file)
            
            # Create TCP socket
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            
            # Bind socket
            self.socket.bind((self.host, self.port))
            self.socket.listen(5)
            
            logging.info(f"Server started on {self.host}:{self.port}")
            
            # Wrap socket with SSL
            self.socket = context.wrap_socket(
                self.socket,
                server_side=True,
                do_handshake_on_connect=False
            )
            
            self.running = True
            
            while self.running:
                try:
                    client_socket, address = self.socket.accept()
                    client_thread = threading.Thread(
                        target=self.handle_client,
                        args=(client_socket, address)
                    )
                    client_thread.start()
                except ssl.SSLError as e:
                    logging.error(f"SSL Error: {e}")
                except Exception as e:
                    logging.error(f"Error accepting connection: {e}")
                    
        except Exception as e:
            logging.error(f"Server error: {e}")
        finally:
            self.stop()
            
    def stop(self):
        """Stop the server"""
        self.running = False
        if self.socket:
            self.socket.close()
        logging.info("Server stopped")

    def handle_client(self, client_socket: ssl.SSLSocket, address: Tuple[str, int]):
        """Handle individual client connections"""
        try:
            logging.info(f"New connection from {address}")
            while self.running:
                data = client_socket.recv(1024)
                if not data:
                    break
                # Process data here
                response = "Server received: " + data.decode('utf-8')
                client_socket.send(response.encode('utf-8'))
        except ssl.SSLError as e:
            logging.error(f"SSL Error with client {address}: {e}")
        except Exception as e:
            logging.error(f"Error handling client {address}: {e}")
        finally:
            client_socket.close()
            logging.info(f"Connection closed for {address}")

if __name__ == "__main__":
    # Example usage with certificate and key files
    server = SecureTCPServer(cert_file="path/to/cert.pem", key_file="path/to/key.pem")
    server.start