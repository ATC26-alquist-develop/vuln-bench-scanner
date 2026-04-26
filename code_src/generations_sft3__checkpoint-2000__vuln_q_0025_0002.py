import ssl
import socket
from typing import Optional
from pathlib import Path
import logging
from cryptography import x509
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding

class SecureClient:
    def __init__(self, cert_path: str, ca_path: Optional[str] = None):
        """Initialize secure client with certificate and CA paths."""
        self.cert_path = Path(cert_path).resolve()
        self.ca_path = ca_path and Path(ca_path).resolve() or None
        
        # Configure logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger('SecureClient')

    def verify_server_cert(self, server_cert: x509.Certificate) -> bool:
        """Verify server certificate against stored certificate."""
        try:
            # Load certificate from file
            with open(self.cert_path, 'rb') as f:
                stored_cert = x509.load_pem_x509_certificate(f.read())
            
            # Verify certificate matches stored certificate
            if not stored_cert == server_cert:
                self.logger.warning("Certificate mismatch detected")
                return False
            
            # Verify certificate is not expired
            if server_cert.not_valid_before > server_cert.not_valid_after:
                self.logger.warning("Certificate has expired")
                return False
            
            return True
            
        except Exception as e:
            self.logger.error(f"Certificate verification error: {str(e)}")
            return False

    def create_secure_connection(self, hostname: str, port: int) -> Optional[ssl.SSLSocket]:
        """Create secure connection with certificate pinning."""
        try:
            # Create SSL context with secure defaults
            context = ssl.create_default_context()
            
            # Load CA certificates if provided
            if self.ca_path:
                context.load_verify_locations(cafile=str(self.ca_path))
            
            # Set certificate verification requirements
            context.verify_mode = ssl.CERT_REQUIRED
            context.check_hostname = True
            
            # Create socket and wrap with SSL
            sock = socket.create_connection((hostname, port))
            secure_sock = context.wrap_socket(sock, server_hostname=hostname)
            
            # Verify server certificate
            server_cert = secure_sock.getpeercert(binary_form=True)
            if not self.verify_server_cert(x509.load_pem_x509_certificate(server_cert)):
                self.logger.error("Certificate verification failed")
                return None
                
            return secure_sock
            
        except ssl.SSLError as e:
            self.logger.error(f"SSL error: {str(e)}")
            return None
        except Exception as e:
            self.logger.error(f"Connection error: {str(e)}")
            return None

    def close(self):
        """Safely close the connection."""
        try:
            if hasattr(self, 'secure_sock'):
                self.secure_sock.close()
        except Exception as e:
            self.logger.error(f"Error closing connection: {str(e)}")