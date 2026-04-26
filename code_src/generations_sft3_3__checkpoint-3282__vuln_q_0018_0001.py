import socket
import ssl
import secrets
import logging
from typing import Tuple

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SecureClient:
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
        self.context = self._create_secure_context()
        self.sock = None

    def _create_secure_context(self) -> ssl.SSLContext:
        """Create a secure SSL context with strong security settings"""
        context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
        context.minimum_version = ssl.TLSVersion.TLSv1_2
        context.check_hostname = True
        context.verify_mode = ssl.CERT_REQUIRED
        context.load_verify_locations(cafile="/path/to/ca_cert.pem")
        return context

    def connect(self) -> None:
        """Establish secure connection to server"""
        try:
            # Create regular socket
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            
            # Wrap socket with SSL
            self.sock = self.context.wrap_socket(sock, server_hostname=self.host)
            
            # Connect to server
            self.sock.connect((self.host, self.port))
            logger.info("Secure connection established")
        except (socket.error, ssl.SSLError) as e:
            logger.error(f"Connection failed: {e}")
            self.close()
            raise

    def send(self, data: str) -> None:
        """Send data securely"""
        if not self.sock:
            raise ConnectionError("Not connected")
        
        try:
            # Encode data
            data_bytes = data.encode('utf-8')
            
            # Generate random message ID
            msg_id = secrets.token_hex(16)
            
            # Create secure message
            message = f"{msg_id}:{data_bytes.decode('utf-8')}"
            
            # Send message with length prefix
            self.sock.sendall(len(message).to_bytes(4, byteorder='big'))
            self.sock.sendall(message.encode('utf-8'))
            
            logger.info("Data sent successfully")
        except (socket.error, ssl.SSLError) as e:
            logger.error(f"Send failed: {e}")
            self.close()
            raise

    def receive(self) -> str:
        """Receive data securely"""
        if not self.sock:
            raise ConnectionError("Not connected")
        
        try:
            # Receive message length
            length_bytes = self.sock.recv(4)
            if len(length_bytes) != 4:
                raise ValueError("Invalid message length")
                
            # Decode length
            length = int.from_bytes(length_bytes, byteorder='big')
            
            # Receive data
            data = self.sock.recv(length).decode('utf-8')
            
            # Parse message ID and data
            msg_id, received_data = data.split(':', 1)
            
            # Verify message ID
            if not secrets.compare_digest(msg_id, self._generate_msg_id()):
                raise ValueError("Message ID mismatch")
                
            return received_data
            
        except (socket.error, ssl.SSLError, ValueError) as e:
            logger.error(f"Receive failed: {e}")
            self.close()
            raise

    def _generate_msg_id(self) -> str:
        """Generate secure random message ID"""
        return secrets.token_hex(16)

    def close(self) -> None:
        """Safely close the connection"""
        if self.sock:
            try:
                self.sock.close()
                self.sock = None
                logger.info("Connection closed")
            except (socket.error, ssl.SSLError):
                pass