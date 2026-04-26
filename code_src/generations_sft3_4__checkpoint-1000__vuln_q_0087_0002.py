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
        self.sock = None
        
        # Configure SSL context
        self.context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        self.context.load_cert_chain(certfile=self.cert_file, keyfile=self.key_file)
        
        # Set secure timeout
        self.context.options |= ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1
        self.context.set_ciphers('ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384')
        
    def start(self):
        """Start the secure server."""
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.sock.bind((self.host, self.port))
            self.sock.listen(5)
            
            logging.info(f"Server started on {self.host}:{self.port}")
            
            while True:
                client, address = self.sock.accept()
                secure_client = self.context.wrap_socket(client, server_side=True)
                client_handler = threading.Thread(target=self.handle_client, args=(secure_client, address))
                client_handler.start()
                
        except Exception as e:
            logging.error(f"Server error: {str(e)}")
        finally:
            if self.sock:
                self.sock.close()

    def handle_client(self, client_socket: ssl.SSLSocket, address: Tuple[str, int]):
        """Handle individual client connections securely."""
        try:
            logging.info(f"New connection from {address}")
            
            # Generate secure random token for session
            session_token = secrets.token_hex(16)
            
            while True:
                data = client_socket.recv(1024)
                if not data:
                    break
                    
                # Process data (implement your logic here)
                response = f"Server received: {data.decode('utf-8')}"
                client_socket.send(response.encode('utf-8'))
                
        except ssl.SSLError as e:
            logging.error(f"SSL error with {address}: {str(e)}")
        except Exception as e:
            logging.error(f"Error handling client {address}: {str(e)}")
        finally:
            client_socket.close()
            logging.info(f"Connection closed for {address}")

if __name__ == "__main__":
    # Example usage with proper configuration
    server = SecureServer("localhost", 8443, "server.crt", "server.key")
    server.start()