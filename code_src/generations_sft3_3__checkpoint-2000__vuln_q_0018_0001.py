import socket
import ssl
import secrets
import logging
from typing import Tuple

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class SecureClientServer:
    def __init__(self, host: str, port: int, cert_path: str, key_path: str):
        """Initialize secure client-server with TLS"""
        self.host = host
        self.port = port
        self.cert_path = cert_path
        self.key_path = key_path
        
        # Generate secure random token for handshake
        self.token = secrets.token_hex(16)
        
        # Configure TLS context
        self.context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        self.context.load_cert_chain(certfile=self.cert_path, keyfile=self.key_path)
        
    def start_server(self) -> None:
        """Start secure server"""
        try:
            # Create socket
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
                server_socket.bind((self.host, self.port))
                server_socket.listen(1)
                logging.info(f"Server listening on {self.host}:{self.port}")
                
                # Accept connection
                with server_socket:
                    conn, addr = server_socket.accept()
                    with self.context.wrap_socket(conn, server_side=True) as secure_conn:
                        logging.info(f"Secure connection from {addr}")
                        self.handle_client(secure_conn)
                        
        except Exception as e:
            logging.error(f"Server error: {str(e)}")

    def start_client(self) -> None:
        """Start secure client"""
        try:
            # Create socket
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
                # Wrap socket with TLS
                with self.context.wrap_socket(client_socket, server_hostname=self.host) as secure_socket:
                    secure_socket.connect((self.host, self.port))
                    self.handle_server(secure_socket)
                    
        except Exception as e:
            logging.error(f"Client error: {str(e)}")

    def handle_client(self, secure_conn: ssl.SSLSocket) -> None:
        """Handle client communication"""
        try:
            # Send token for handshake
            secure_conn.sendall(self.token.encode())
            
            # Receive and process data
            data = secure_conn.recv(1024)
            if data:
                logging.info(f"Received data: {data.decode()}")
                
        except ssl.SSLError as e:
            logging.error(f"SSL error: {str(e)}")
        except Exception as e:
            logging.error(f"Error handling client: {str(e)}")

    def handle_server(self, secure_conn: ssl.SSLSocket) -> None:
        """Handle server communication"""
        try:
            # Receive and process data
            data = secure_conn.recv(1024)
            if data:
                logging.info(f"Received data: {data.decode()}")
                
        except ssl.SSLError as e:
            logging.error(f"SSL error: {str(e)}")
        except Exception as e:
            logging.error(f"Error handling server: {str(e)}")

if __name__ == "__main__":
    # Example usage
    server = SecureClientServer("localhost", 8443, "server.crt", "server.key")
    server.start_server()