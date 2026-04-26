import socket
import ssl
import logging
from typing import Tuple
from threading import Thread
import secrets

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class SecureServer:
    def __init__(self, host: str = '0.0.0.0', port: int = 8443):
        self.host = host
        self.port = port
        self.socket = None
        self.context = None
        
    def setup_ssl_context(self) -> None:
        """Set up secure SSL context with strong security settings"""
        # Create SSL context with secure defaults
        self.context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        self.context.options |= ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1  # Disable older TLS versions
        self.context.set_ciphers('ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384')
        self.context.options |= ssl.OP_NO_COMPRESSION  # Prevent downgrade attacks
        self.context.verify_mode = ssl.CERT_REQUIRED  # Require server certificate
        self.context.check_hostname = True
        self.context.load_cert_chain(certfile='server.crt', keyfile='server.key')

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
            
            # Set non-blocking mode
            self.socket.setblocking(False)
            
            logging.info(f"Server started on {self.host}:{self.port}")
            
            while True:
                try:
                    # Accept connection
                    client_socket, address = self.socket.accept()
                    logging.info(f"New connection from {address}")
                    
                    # Wrap socket with SSL
                    secure_client = self.context.wrap_socket(client_socket, server_side=True)
                    
                    # Handle connection in separate thread
                    client_thread = Thread(target=self.handle_client, args=(secure_client, address))
                    client_thread.start()
                    
                except ssl.SSLError as e:
                    logging.error(f"SSL error: {e}")
                except Exception as e:
                    logging.error(f"Error accepting connection: {e}")
                    
        except Exception as e:
            logging.error(f"Server error: {e}")
        finally:
            if self.socket:
                self.socket.close()

    def handle_client(self, client_socket: ssl.SSLSocket, address: Tuple[str, int]) -> None:
        """Handle client connections"""
        try:
            # Generate unique session token
            session_token = secrets.token_hex(16)
            
            # Send session token to client
            client_socket.sendall(session_token.encode())
            
            # Handle client requests
            while True:
                data = client_socket.recv(1024)
                if not data:
                    break
                
                # Process received data (implement your logic here)
                response = f"Server received: {data.decode()}"
                client_socket.sendall(response.encode())
                
        except ssl.SSLError as e:
            logging.error(f"SSL error with {address}: {e}")
        except Exception as e:
            logging.error(f"Error handling client {address}: {e}")
        finally:
            client_socket.close()
            logging.info(f"Connection closed for {address}")

if __name__ == "__main__":
    server = SecureServer()
    server.setup_ssl_context()
    server.start()