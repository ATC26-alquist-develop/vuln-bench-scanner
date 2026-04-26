import socket
import ssl
import secrets
import logging
from typing import Tuple, Optional

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class SecureSocket:
    def __init__(self, host: str, port: int, cert_path: str, key_path: str):
        """Initialize secure socket with TLS"""
        self.host = host
        self.port = port
        self.cert_path = cert_path
        self.key_path = key_path
        self.sock: Optional[ssl.SSLSocket] = None
        
    def start_server(self) -> None:
        """Start secure server"""
        try:
            # Create SSL context with secure defaults
            context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
            context.load_cert_chain(certfile=self.cert_path, keyfile=self.key_path)
            
            # Create socket and wrap with SSL
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.bind((self.host, self.port))
                sock.listen(1)
                with context.wrap_socket(sock, server_side=True) as secure_sock:
                    logging.info(f"Server started on {self.host}:{self.port}")
                    while True:
                        conn, addr = secure_sock.accept()
                        logging.info(f"New connection from {addr}")
                        self.handle_client(conn, addr)
                        
        except Exception as e:
            logging.error(f"Server error: {str(e)}")
            raise

    def start_client(self) -> None:
        """Start secure client"""
        try:
            # Create SSL context with secure defaults
            context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
            context.check_hostname = False
            context.verify_mode = ssl.CERT_NONE
            
            # Create socket and wrap with SSL
            with socket.create_connection((self.host, self.port)) as sock:
                with context.wrap_socket(sock, server_hostname=self.host) as secure_sock:
                    logging.info(f"Connected to {self.host}:{self.port}")
                    self.handle_client(secure_sock)
                    
        except Exception as e:
            logging.error(f"Client error: {str(e)}")
            raise

    def handle_client(self, sock: ssl.SSLSocket, addr: Tuple[str, int] = None) -> None:
        """Handle client connection securely"""
        try:
            # Generate random session token
            session_token = secrets.token_hex(16)
            logging.info(f"Session token: {session_token}")
            
            while True:
                data = sock.recv(1024)
                if not data:
                    break
                    
                # Process received data (implement your logic here)
                response = self.process_data(data)
                
                # Send response
                sock.sendall(response)
                
        except ssl.SSLError as e:
            logging.error(f"SSL error: {str(e)}")
        except Exception as e:
            logging.error(f"Error handling client: {str(e)}")
        finally:
            logging.info(f"Connection closed for {addr}")
            sock.close()

    def process_data(self, data: bytes) -> bytes:
        """Process received data (implement your logic here)"""
        # Implement your data processing logic
        return b"Processed: " + data