import socket
import ssl
import threading
import logging
from typing import Tuple

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class SecureServer:
    def __init__(self, host: str = '0.0.0.0', port: int = 8443):
        self.host = host
        self.port = port
        self.socket = None
        self.context = None
        
    def setup_ssl(self) -> None:
        """Set up secure SSL context"""
        # Create secure SSL context
        self.context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        self.context.load_cert_chain(certfile="server.crt", keyfile="server.key")
        
        # Enforce TLS 1.2 or higher
        self.context.minimum_version = ssl.TLSVersion.TLSv1_2
        
    def start(self) -> None:
        """Start the secure server"""
        try:
            # Create TCP socket
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            
            # Bind socket to address
            self.socket.bind((self.host, self.port))
            
            # Start listening for connections
            self.socket.listen(5)
            
            # Set timeout for accept operations
            self.socket.settimeout(30)
            
            logging.info(f"Server started on {self.host}:{self.port}")
            
            while True:
                try:
                    client_socket, address = self.socket.accept()
                    # Wrap socket with SSL
                    secure_client = self.context.wrap_socket(client_socket, server_side=True)
                    
                    # Start new thread for each connection
                    client_thread = threading.Thread(
                        target=self.handle_client,
                        args=(secure_client, address)
                    )
                    client_thread.start()
                    
                except socket.timeout:
                    logging.info("Server timeout - waiting for new connections")
                except Exception as e:
                    logging.error(f"Error accepting connection: {str(e)}")
                    
        except Exception as e:
            logging.error(f"Server error: {str(e)}")
        finally:
            if self.socket:
                self.socket.close()

    def handle_client(self, client_socket: ssl.SSLSocket, address: Tuple[str, int]) -> None:
        """Handle client connections"""
        try:
            logging.info(f"New connection from {address[0]}:{address[1]}")
            
            # Set timeout for client operations
            client_socket.settimeout(30)
            
            while True:
                try:
                    data = client_socket.recv(1024)
                    if not data:
                        break
                    
                    # Process received data (implement your logic here)
                    response = "Server received: " + data.decode('utf-8')
                    
                    # Send response
                    client_socket.send(response.encode('utf-8'))
                    
                except ssl.SSLError as e:
                    logging.error(f"SSL error with client {address}: {str(e)}")
                    break
                except Exception as e:
                    logging.error(f"Error handling client {address}: {str(e)}")
                    break
                    
        except Exception as e:
            logging.error(f"Error in client handler: {str(e)}")
        finally:
            client_socket.close()
            logging.info(f"Connection closed for {address[0]}:{address[1]}")

if __name__ == "__main__":
    server = SecureServer()
    server.setup_ssl()
    server.start()