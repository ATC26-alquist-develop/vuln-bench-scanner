```python
import socket
import ssl
import secrets
import logging
from typing import Tuple

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SecureClientServer:
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
        self.context = self._create_secure_context()
        
    def _create_secure_context(self) -> ssl.SSLContext:
        """Create a secure SSL context with strong security settings"""
        context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        context.options |= ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1  # Disable older TLS versions
        context.set_ciphers('ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384')
        context.set_ecdh_curve('prime256v1')
        context.check_hostname = True
        context.verify_mode = ssl.CERT_REQUIRED
        return context

    def _generate_secure_random_port(self) -> int:
        """Generate a random port number for secure communication"""
        return secrets.randbelow(65535) + 10000  # Avoid common ports

    def start_server(self) -> None:
        """Start a secure server"""
        try:
            # Generate a random port
            random_port = self._generate_secure_random_port()
            
            # Create socket
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.bind((self.host, random_port))
                sock.listen(1)
                
                # Wrap socket with SSL
                with self.context.wrap_socket(sock, server_side=True) as secure_sock:
                    logger.info(f"Server started on port {random_port}")
                    
                    while True:
                        conn, addr = secure_sock.accept()
                        self._handle_client(conn, addr)
                        
        except Exception as e:
            logger.error(f"Server error: {str(e)}")
            raise

    def _handle_client(self, conn: ssl.SSLSocket, addr: Tuple[str, int]) -> None:
        """Handle client connection securely"""
        try:
            logger.info(f"New connection from {addr}")
            
            # Receive data with timeout
            data = conn.recv(1024)
            if not data:
                return
            
            # Process data (example: echo back)
            response = f"Server received: {data.decode('utf-8')}"
            
            # Send response
            conn.sendall(response.encode('utf-8'))
            
        except ssl.SSLError as e:
            logger.error(f"SSL error with {addr}: {str(e)}")
        except Exception as e:
            logger.error(f"Error handling client {addr}: {str(e)}")
        finally:
            conn.close()

    def start_client(self) -> None:
        """Start a secure client"""
        try:
            # Create socket
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                # Wrap socket with SSL
                with self.context.wrap_socket(sock, server_hostname=self.host) as secure_sock:
                    logger.info(f"Client connecting to {self.host}:{self.port}")
                    
                    # Connect
                    secure_sock.connect((self.host, self.port))
                    
                    # Send data
                    message = "Hello, secure server!"
                    secure_sock.sendall(message.encode('utf-8'))
                    
                    # Receive response
                    response = secure_sock.recv(1024)
                    logger.info(f"Received: {response.decode('utf-8')}")
                    
        except ssl.SSLError as e:
            logger.error(f"SSL error: {str(e)}")
        except Exception as e:
            logger.error(f"Error in client: {str(e)}")

if __