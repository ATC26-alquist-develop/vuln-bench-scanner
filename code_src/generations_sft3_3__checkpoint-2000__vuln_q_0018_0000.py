import socket
import ssl
import logging
from typing import Tuple
from contextlib import contextmanager

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SecureSocketConnection:
    def __init__(self, host: str, port: int, ca_cert_path: str):
        """Initialize secure socket connection with proper security measures."""
        self.host = host
        self.port = port
        self.ca_cert_path = ca_cert_path
        self.socket = None
        self.context = None
        
    @contextmanager
    def create_secure_connection(self):
        """Create and manage secure socket connection with proper cleanup."""
        try:
            # Create SSL context with secure defaults
            self.context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH, cafile=self.ca_cert_path)
            self.context.check_hostname = True
            self.context.verify_mode = ssl.CERT_REQUIRED
            
            # Create socket
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            
            # Wrap socket with SSL
            secure_socket = self.context.wrap_socket(
                self.socket,
                server_hostname=self.host
            )
            
            logger.info(f"Established secure connection to {self.host}:{self.port}")
            yield secure_socket
            
        except (socket.error, ssl.SSLError) as e:
            logger.error(f"Connection error: {str(e)}")
            raise
        finally:
            if self.socket:
                try:
                    self.socket.close()
                except:
                    pass
                self.socket = None
            if self.context:
                try:
                    self.context.close()
                except:
                    pass
                self.context = None

    def send_data(self, data: str) -> Tuple[bool, str]:
        """Safely send data over the secure connection."""
        if not self.socket:
            logger.error("No active connection")
            return False, ""
            
        try:
            # Encode data to bytes with proper encoding
            data_bytes = data.encode('utf-8')
            self.socket.sendall(data_bytes)
            return True, "Data sent successfully"
        except (socket.error, ssl.SSLError) as e:
            logger.error(f"Error sending data: {str(e)}")
            return False, "Failed to send data"

    def receive_data(self, max_size: int = 1024) -> Tuple[bool, str]:
        """Safely receive data from the secure connection."""
        if not self.socket:
            logger.error("No active connection")
            return False, ""
            
        try:
            data = self.socket.recv(max_size)
            if data:
                return True, data.decode('utf-8')
            return True, "No data received"
        except (socket.error, ssl.SSLError) as e:
            logger.error(f"Error receiving data: {str(e)}")
            return False, "Failed to receive data"

def main():
    # Example usage
    try:
        connection = SecureSocketConnection("example.com", 443, "/path/to/ca_cert.pem")
        with connection.create_secure_connection() as secure_socket:
            # Send data
            success, result = connection.send_data("GET / HTTP/1.1\r\nHost: example.com\r\n\r\n")
            if success:
                logger.info(f"Send result: {result}")
                
            # Receive data
            success, result = connection.receive_data()
            if success:
                logger.info(f"Received data: {result}")
                
    except Exception as e:
        logger.error(f"Error: {str(e)}")

if __name__ == "__main__":
    main()