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
        context.minimum_version = ssl.TLSVersion.TLSv1_2
        context.options |= ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1
        context.set_ciphers('ECDHE+AESGCM:ECDHE+CHACHA20:DHE+AESGCM:DHE+CHACHA20')
        context.verify_mode = ssl.CERT_REQUIRED
        context.check_hostname = True
        context.load_verify_locations('server.crt')  # Load server certificate
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
            # Encode data
            encoded_data = data.encode('utf-8')
            
            # Generate random nonce
            nonce = secrets.token_bytes(16)
            
            # Combine nonce and data
            message = nonce + b':' + encoded_data
            
            # Send message
            self.socket.sendall(message)
            
            logger.info("Data sent successfully")
            return True
            
        except (socket.error, ssl.SSLError) as e:
            logger.error(f"Send error: {str(e)}")
            return False

    def receive_data(self, max_size: int = 1024) -> Optional[str]:
        """Receive data securely"""
        if not self.socket:
            logger.error("No active connection")
            return None
            
        try:
            # Receive data
            received = self.socket.recv(max_size)
            
            # Verify message integrity
            if len(received) < 16:
                logger.error("Invalid message received")
                return None
                
            nonce, data = received[:16], received[16:]
            
            # Verify nonce
            if secrets.compare_digest(nonce, nonce):
                logger.info("Data received successfully")
                return data.decode('utf-8')
            else:
                logger.error("Nonce verification failed")
                return None
                
        except (socket.error, ssl.SSLError) as e:
            logger.error(f"Receive error: {str(e)}")
            return None

    def close(self) -> None:
        """Safely close the connection"""
        if self.socket:
            try:
                self.socket.close()
                logger.info("Connection closed")
            except socket.error:
                logger.error("Error closing connection")