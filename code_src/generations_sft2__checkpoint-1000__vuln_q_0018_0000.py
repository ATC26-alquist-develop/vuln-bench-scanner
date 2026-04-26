import socket
import ssl
import logging
from typing import Optional
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SecureSocketClient:
    def __init__(self, host: str, port: int):
        """Initialize secure socket client with host and port."""
        if not isinstance(host, str) or not isinstance(port, int):
            raise ValueError("Invalid input types")
        if port < 1 or port > 65535:
            raise ValueError("Port must be between 1 and 65535")
        
        self.host = host
        self.port = port
        self.context = ssl.create_default_context()
        self.context.options |= ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1  # Disable older TLS versions
        self.context.set_ciphers('ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384')
        self.context.verify_mode = ssl.CERT_REQUIRED
        self.context.check_hostname = True

    def connect(self) -> Optional[ssl.SSLSocket]:
        """Establish secure connection to server."""
        try:
            with socket.create_connection((self.host, self.port), timeout=10) as sock:
                with self.context.wrap_socket(sock, server_hostname=self.host) as secure_sock:
                    logger.info(f"Connected to {self.host}:{self.port}")
                    return secure_sock
        except (socket.error, ssl.SSLError) as e:
            logger.error(f"Connection failed: {str(e)}")
            return None

    def close(self):
        """Close the connection safely."""
        if hasattr(self, 'secure_sock'):
            self.secure_sock.close()
            logger.info("Connection closed")

def main():
    """Main function to demonstrate secure socket usage."""
    try:
        # Get credentials from environment variables
        host = os.environ.get('SERVER_HOST')
        port = int(os.environ.get('SERVER_PORT', 443))
        
        if not host or not port:
            raise ValueError("Missing required environment variables")
            
        client = SecureSocketClient(host, port)
        secure_sock = client.connect()
        
        if secure_sock:
            # Example: Send a simple message
            secure_sock.sendall(b"Hello, server!")
            
            # Receive response
            data = secure_sock.recv(1024)
            logger.info(f"Received: {data.decode('utf-8')}")
            
            client.close()
            
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()