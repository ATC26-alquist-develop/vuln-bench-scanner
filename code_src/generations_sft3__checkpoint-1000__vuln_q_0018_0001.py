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
        context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
        context.options |= ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1  # Disable older TLS versions
        context.set_ciphers('ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384')
        context.check_hostname = True
        context.verify_mode = ssl.CERT_REQUIRED
        return context

    def _create_secure_socket(self) -> ssl.SSLSocket:
        """Create a secure SSL socket"""
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        return self.context.wrap_socket(sock, server_hostname=self.host)

    def start_server(self) -> None:
        """Start a secure server"""
        try:
            with self._create_secure_socket() as server_socket:
                server_socket.bind((self.host, self.port))
                server_socket.listen(5)
                logger.info(f"Server listening on {self.host}:{self.port}")
                
                while True:
                    client_socket, addr = server_socket.accept()
                    logger.info(f"Accepted connection from {addr}")
                    self._handle_client(client_socket)
        except Exception as e:
            logger.error(f"Server error: {e}")
            raise

    def _handle_client(self, client_socket: ssl.SSLSocket) -> None:
        """Handle client connection securely"""
        try:
            # Generate a secure random token for session
            session_token = secrets.token_hex(16)
            
            # Send session token to client
            client_socket.sendall(session_token.encode('utf-8'))
            
            # Receive data from client
            data = client_socket.recv(1024)
            if not data:
                return
            
            # Process received data (example: echo back)
            response = f"Received: {data.decode('utf-8')}"
            client_socket.sendall(response.encode('utf-8'))
            
        except ssl.SSLError as e:
            logger.error(f"SSL error: {e}")
        except Exception as e:
            logger.error(f"Error handling client: {e}")
        finally:
            client_socket.close()

    def start_client(self, server_host: str, server_port: int) -> None:
        """Start a secure client"""
        try:
            with self._create_secure_socket() as client_socket:
                client_socket.connect((server_host, server_port))
                logger.info(f"Connected to {server_host}:{server_port}")
                
                # Receive session token
                session_token = client_socket.recv(1024).decode('utf-8')
                logger.info(f"Received session token: {session_token}")
                
                # Send data to server
                message = f"Secure message from client {session_token}"
                client_socket.sendall(message.encode('utf-8'))
                
                # Receive response
                response = client_socket.recv(1024).decode('utf-8')
                logger.info(f"Received response: {response}")
                
        except ssl.SSLError as e:
            logger.error(f"SSL error: {e}")
        except Exception as e:
            logger.error(f"Error in client: {e}")
        finally:
            client_socket.close()

if __name__ == "__main__":
    # Example usage
    server = SecureClient