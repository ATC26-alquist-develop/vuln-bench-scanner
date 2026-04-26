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
        self.sock = None
        self.context = None
        
    def start_server(self) -> None:
        """Start secure server"""
        try:
            # Create SSL context
            self.context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
            self.context.load_cert_chain(certfile=self.cert_path, keyfile=self.key_path)
            
            # Create socket
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            
            # Bind socket
            sock.bind((self.host, self.port))
            sock.listen(5)
            
            logging.info(f"Server started on {self.host}:{self.port}")
            
            while True:
                client_sock, addr = sock.accept()
                secure_client = self.context.wrap_socket(client_sock, server_side=True)
                self.handle_client(secure_client, addr)
                
        except Exception as e:
            logging.error(f"Server error: {str(e)}")
        finally:
            if self.sock:
                self.sock.close()
            if self.context:
                self.context = None
            if sock:
                sock.close()

    def handle_client(self, client: ssl.SSLSocket, addr: Tuple[str, int]) -> None:
        """Handle client connection"""
        try:
            logging.info(f"New connection from {addr}")
            while True:
                data = client.recv(1024)
                if not data:
                    break
                # Process data here
                response = "Received: " + data.decode('utf-8')
                client.send(response.encode('utf-8'))
        except ssl.SSLError as e:
            logging.error(f"SSL error with {addr}: {str(e)}")
        except Exception as e:
            logging.error(f"Error handling client {addr}: {str(e)}")
        finally:
            client.close()
            logging.info(f"Connection closed for {addr}")

    def start_client(self, host: str, port: int) -> None:
        """Start secure client"""
        try:
            # Create SSL context
            context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
            context.check_hostname = False
            context.verify_mode = ssl.CERT_NONE  # In production, use proper certificate verification
            
            # Create socket
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            
            # Wrap socket with SSL
            secure_sock = context.wrap_socket(sock, server_hostname=host)
            
            secure_sock.connect((host, port))
            logging.info(f"Connected to {host}:{port}")
            
            while True:
                message = input("Enter message: ")
                secure_sock.send(message.encode('utf-8'))
                data = secure_sock.recv(1024)
                print(f"Received: {data.decode('utf-8')}")
                
        except ssl.SSLError as e:
            logging.error(f"SSL error: {str(e)}")
        except Exception as e:
            logging.error(f"Error: {str(e)}")
        finally:
            if secure_sock:
                secure_sock.close()