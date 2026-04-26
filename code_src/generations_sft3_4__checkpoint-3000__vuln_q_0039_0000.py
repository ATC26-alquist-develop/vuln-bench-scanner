import socket
import ssl
import threading
import logging
from typing import Tuple

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SecureServer:
    def __init__(self, host: str = '0.0.0.0', port: int = 8443):
        self.host = host
        self.port = port
        self.socket = None
        self.context = None
        
    def setup_ssl(self) -> None:
        """Set up secure SSL context"""
        # Use strong TLS configuration
        self.context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        self.context.options |= ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1  # Disable older TLS versions
        self.context.set_ciphers('ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384')
        self.context.options |= ssl.OP_NO_COMPRESSION  # Prevent downgrade attacks
        self.context.verify_mode = ssl.CERT_REQUIRED  # Require client certificates
        self.context.load_verify_locations('server.crt')  # Load valid certificate
        self.context.load_cert_chain(certfile='server.crt', keyfile='server.key')  # Load private key

    def start(self) -> None:
        """Start the secure server"""
        try:
            # Create socket
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            
            # Bind socket
            self.socket.bind((self.host, self.port))
            self.socket.listen(5)
            
            # Set non-blocking
            self.socket.setblocking(0)
            
            logger.info(f"Server started on {self.host}:{self.port}")
            
            while True:
                try:
                    # Accept connections
                    client_socket, address = self.socket.accept()
                    logger.info(f"New connection from {address}")
                    
                    # Wrap with SSL
                    secure_client = self.context.wrap_socket(client_socket, server_side=True)
                    
                    # Handle client in separate thread
                    client_thread = threading.Thread(target=self.handle_client, 
                                                     args=(secure_client, address))
                    client_thread.start()
                    
                except ssl.SSLError as e:
                    logger.error(f"SSL error: {e}")
                except Exception as e:
                    logger.error(f"Error accepting connection: {e}")
                    
        except Exception as e:
            logger.error(f"Server error: {e}")
        finally:
            if self.socket:
                self.socket.close()

    def handle_client(self, client_socket: ssl.SSLSocket, address: Tuple[str, int]) -> None:
        """Handle client connections"""
        try:
            while True:
                data = client_socket.recv(1024)
                if not data:
                    break
                    
                # Process data here
                response = "Received: " + data.decode('utf-8')
                client_socket.send(response.encode('utf-8'))
                
        except ssl.SSLError as e:
            logger.error(f"SSL error with client {address}: {e}")
        except Exception as e:
            logger.error(f"Error handling client {address}: {e}")
        finally:
            client_socket.close()
            logger.info(f"Connection closed for {address}")

if __name__ == "__main__":
    server = SecureServer()
    server.setup_ssl()
    server.start()