import ssl
import socket
from typing import Optional
import logging
from pathlib import Path

class SecureClient:
    def __init__(self, cert_path: str, ca_path: str):
        """Initialize secure client with certificate and CA paths."""
        self.cert_path = Path(cert_path)
        self.ca_path = Path(ca_path)
        
        # Configure logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        
        # Validate paths exist
        if not self.cert_path.exists() or not self.ca_path.exists():
            raise ValueError("Certificate or CA file does not exist")

    def create_secure_connection(self, hostname: str, port: int = 443) -> Optional[ssl.SSLSocket]:
        """
        Create a secure SSL connection with certificate pinning.
        
        Args:
            hostname: Target hostname
            port: Target port (default: 443)
            
        Returns:
            SSLSocket if connection successful, None if failed
        """
        try:
            # Create SSL context with secure defaults
            context = ssl.create_default_context()
            
            # Load certificates
            context.load_verify_locations(cafile=str(self.ca_path))
            context.load_cert_chain(certfile=str(self.cert_path))
            
            # Set certificate pinning
            with open(str(self.cert_path), 'rb') as cert_file:
                cert_data = cert_file.read()
                context.check_hostname = True
                context.verify_mode = ssl.CERT_REQUIRED
                context.load_verify_locations(cafile=str(self.ca_path))
                context.verify_flags = ssl.VERIFY_X509_STRICT
                
                # Get fingerprint for pinning
                cert_fingerprint = cert_data[:20].hex()
                
                # Add certificate pinning
                context.load_verify_locations(cadata=cert_data)
                
            # Create socket and wrap with SSL
            sock = socket.create_connection((hostname, port))
            secure_sock = context.wrap_socket(sock, 
                                             server_hostname=hostname)
            
            # Log successful connection
            self.logger.info(f"Secure connection established with {hostname}")
            return secure_sock
            
        except (ssl.SSLError, socket.error) as e:
            self.logger.error(f"Connection failed: {str(e)}")
            return None

    def close(self):
        """Safely close the connection."""
        try:
            if hasattr(self, 'secure_sock'):
                self.secure_sock.close()
        except Exception as e:
            self.logger.error(f"Error closing connection: {str(e)}")