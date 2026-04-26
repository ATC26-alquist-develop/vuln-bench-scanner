```python
import socket
import ssl
import secrets
import logging
from typing import Tuple, Optional

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class SecureClient:
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
        self.context = self._create_secure_context()
        self.sock = None

    def _create_secure_context(self) -> ssl.SSLContext:
        """Create a secure SSL context"""
        context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
        context.minimum_version = ssl.TLSVersion.TLSv1_2
        context.verify_mode = ssl.CERT_REQUIRED
        context.check_hostname = True
        context.load_verify_locations(cafile="path/to/ca_cert.pem")
        return context

    def connect(self) -> bool:
        """Establish secure connection"""
        try:
            # Create socket
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            
            # Wrap socket with SSL
            self.sock = self.context.wrap_socket(sock, server_hostname=self.host)
            
            # Attempt connection
            self.sock.connect((self.host, self.port))
            logging.info("Secure connection established")
            return True
        except (socket.error, ssl.SSLError) as e:
            logging.error(f"Connection failed: {str(e)}")
            return False

    def send_data(self, data: str) -> bool:
        """Send data securely"""
        if not self.sock:
            logging.error("Not connected")
            return False
            
        try:
            # Encode data
            encoded_data = data.encode('utf-8')
            
            # Generate random nonce
            nonce = secrets.token_bytes(16)
            
            # Combine data with nonce
            message = f"{nonce.hex()}:{encoded_data.decode()}"
            
            # Send message
            self.sock.sendall(message.encode('utf-8'))
            logging.info("Data sent successfully")
            return True
        except (socket.error, ssl.SSLError) as e:
            logging.error(f"Send failed: {str(e)}")
            return False

    def receive_data(self) -> Optional[str]:
        """Receive data securely"""
        if not self.sock:
            logging.error("Not connected")
            return None
            
        try:
            # Receive data
            data = self.sock.recv(4096)
            
            if not data:
                logging.warning("Connection closed by server")
                return None
                
            # Extract nonce and data
            nonce, received_data = data.decode().split(':', 1)
            
            # Verify nonce
            if not secrets.compare_digest(nonce, bytes.fromhex(nonce.hex())):
                logging.error("Nonce verification failed")
                return None
                
            # Decode and return data
            return received_data.decode()
        except (socket.error, ssl.SSLError, ValueError) as e:
            logging.error(f"Receive failed: {str(e)}")
            return None

    def close(self) -> None:
        """Safely close connection"""
        if self.sock:
            try:
                self.sock.close()
                logging.info("Connection closed")
            except socket.error:
                pass
            finally:
                self.sock = None

class SecureServer:
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
        self.context = self._create_secure_context()
        self.sock = None

    def _create_secure_context(self) -> ssl.SSLContext:
        """Create a secure SSL context"""
        context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        context.minimum_version = ssl.TLSVersion.TLSv1_2
        context.load_cert_chain(certfile="path/to/cert.pem", keyfile="path/to/key.pem