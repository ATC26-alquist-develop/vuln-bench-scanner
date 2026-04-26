```python
import socket
import ssl
import secrets
import logging
from typing import Tuple, Optional

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SecureClientServer:
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
        self.socket = None
        self.context = None
        
    def create_secure_context(self) -> ssl.SSLContext:
        """Create a secure SSL context with strong security settings"""
        context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
        context.options |= ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1  # Disable older TLS versions
        context.set_ciphers('ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384')
        context.minimum_version = ssl.TLSVersion.TLSv1_2
        context.check_hostname = True
        context.verify_mode = ssl.CERT_REQUIRED
        return context

    def connect(self) -> bool:
        """Establish secure connection to server"""
        try:
            # Create SSL context
            self.context = self.create_secure_context()
            
            # Create socket
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            
            # Wrap socket with SSL
            self.socket = self.context.wrap_socket(self.socket, server_hostname=self.host)
            
            # Connect to server
            self.socket.connect((self.host, self.port))
            
            logger.info("Secure connection established")
            return True
            
        except (socket.error, ssl.SSLError) as e:
            logger.error(f"Connection error: {str(e)}")
            return False

    def send_data(self, data: str) -> bool:
        """Send data securely"""
        try:
            # Encode data
            encoded_data = data.encode('utf-8')
            
            # Generate random nonce
            nonce = secrets.token_bytes(16)
            
            # Create secure message
            secure_message = f"{nonce.hex()}{encoded_data}"
            
            # Send message
            self.socket.sendall(secure_message.encode('utf-8'))
            
            logger.info("Data sent securely")
            return True
            
        except (socket.error, ssl.SSLError) as e:
            logger.error(f"Send error: {str(e)}")
            return False

    def receive_data(self, max_size: int = 1024) -> Optional[str]:
        """Receive data securely"""
        try:
            # Receive data
            received = self.socket.recv(max_size)
            
            if not received:
                logger.warning("No data received")
                return None
                
            # Parse nonce and data
            nonce, data = received.split(b':', 1)
            
            # Verify nonce
            if not secrets.compare_digest(nonce, secrets.token_bytes(16)):
                logger.error("Nonce verification failed")
                return None
                
            # Decode and return data
            return data.decode('utf-8')
            
        except (socket.error, ssl.SSLError) as e:
            logger.error(f"Receive error: {str(e)}")
            return None

    def close(self) -> None:
        """Securely close the connection"""
        try:
            if self.socket:
                self.socket.close()
                logger.info("Connection closed")
        except (socket.error, ssl.SSLError) as e:
            logger.error(f"Error closing connection: {str(e)}")

# Example usage
if __name__ == "__main__":
    client = SecureClientServer("example.com", 443)
    if client.connect():
        client.send_data("Hello, secure server!")
        response = client.receive_data()
        if response:
            print(f"Received: {response}")
        client.close()