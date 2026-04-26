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
        context.load_default_certs(purpose=ssl.Purpose.SERVER_AUTH)
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
        if not self.socket:
            logger.error("No active connection")
            return False
            
        try:
            # Generate random nonce
            nonce = secrets.token_bytes(16)
            
            # Prepare message with nonce
            message = f"{nonce.hex()}:{data}"
            
            # Send message
            self.socket.sendall(message.encode('utf-8'))
            logger.info("Data sent successfully")
            return True
            
        except (socket.error, ssl.SSLError) as e:
            logger.error(f"Send error: {str(e)}")
            return False

    def receive_data(self) -> Optional[str]:
        """Receive data securely"""
        if not self.socket:
            logger.error("No active connection")
            return None
            
        try:
            # Receive message
            raw_data = self.socket.recv(1024)
            
            if not raw_data:
                logger.info("Connection closed by server")
                return None
                
            # Parse nonce and data
            nonce, data = raw_data.decode('utf-8').split(':')
            
            # Verify nonce
            if secrets.compare_digest(nonce, secrets.token_bytes(16).hex()):
                logger.info("Data received successfully")
                return data
                
            logger.warning("Nonce verification failed")
            return None
            
        except (socket.error, ssl.SSLError) as e:
            logger.error(f"Receive error: {str(e)}")
            return None

    def close(self) -> None:
        """Securely close the connection"""
        if self.socket:
            try:
                self.socket.close()
                logger.info("Connection closed")
            except socket.error as e:
                logger.error(f"Error closing connection: {str(e)}")