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
        if not isinstance(port, int) or not (0 <= port < 65536):
            raise ValueError("Port must be an integer between 0 and 65536")
        if not isinstance(host, str):
            raise ValueError("Host must be a string")
            
        # Create secure SSL context
        self.context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        if cert_file and key_file:
            self.context.load_cert_chain(certfile=cert_file, keyfile=key_file)

    def start(self):
        """Start the secure TCP server"""
        try:
            # Create TCP socket
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            
            # Set reuse address to avoid "Address already in use" errors
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            
            # Bind socket to address
            self.socket.bind((self.host, self.port))
            
            # Start listening for connections
            self.socket.listen(5)
            self.running = True
            
            logging.info(f"Server started on {self.host}:{self.port}")
            
            while self.running:
                try:
                    client_socket, address = self.socket.accept()
                    # Wrap socket with SSL
                    secure_client = self.context.wrap_socket(client_socket, server_side=True)
                    
                    # Start new thread for each client
                    client_thread = threading.Thread(
                        target=self.handle_client,
                        args=(secure_client, address)
                    )
                    client_thread.start()
                except ssl.SSLError as e:
                    logging.error(f"SSL error: {e}")
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
                # Process received data here
                response = "Server received: " + data.decode('utf-8')
                client_socket.send(response.encode('utf-8'))
        except ssl.SSLError as e:
            logging.error(f"SSL error with client {address}: {e}")
        except Exception as e:
            logging.error(f"Error handling client {address}: {e}")
        finally:
            client_socket.close()
            logging.info(f"Connection closed for {address}")

if __name__ == "__main__":
    # Example usage with certificate and key
    server = SecureTCPServer(cert_file="path/to/cert.pem", key_file="path/to/key.pem")
    try:
        server.start()
    except KeyboardInterrupt:
        logging.info("Server shutdown requested")
        server.stop()