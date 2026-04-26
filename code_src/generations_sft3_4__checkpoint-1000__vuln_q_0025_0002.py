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

    def create_secure_connection(self, host: str, port: int) -> Optional[ssl.SSLSocket]:
        """
        Create a secure SSL connection with certificate pinning.
        
        Args:
            host: Target hostname
            port: Target port
            
        Returns:
            SSL socket or None if connection fails
        """
        try:
            # Create SSL context with secure defaults
            context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
            
            # Load CA certificates
            context.load_verify_locations(cafile=str(self.ca_path))
            
            # Load client certificate
            context.load_cert_chain(certfile=str(self.cert_path))
            
            # Set certificate verification requirements
            context.verify_mode = ssl.CERT_REQUIRED
            context.check_hostname = True
            
            # Create socket
            sock = socket.create_connection((host, port))
            
            # Wrap socket with SSL
            secure_sock = context.wrap_socket(
                sock,
                server_hostname=host
            )
            
            # Verify certificate matches expected
            if not self._verify_certificate(secure_sock):
                self.logger.error("Certificate verification failed")
                return None
                
            return secure_sock
            
        except (ssl.SSLError, socket.error) as e:
            self.logger.error(f"Connection failed: {str(e)}")
            return None

    def _verify_certificate(self, ssl_sock: ssl.SSLSocket) -> bool:
        """
        Verify certificate matches expected pin.
        
        Args:
            ssl_sock: SSL socket to verify
            
        Returns:
            True if certificate matches pin, False otherwise
        """
        try:
            cert = ssl_sock.getpeercert(binary_form=True)
            cert_hash = cert.get_extension('subjectAltName').value[0].value
            
            # Example pin: expected certificate hash
            expected_hash = "0123456789abcdef0123456789abcdef"
            
            # Verify hash matches expected
            return cert_hash == expected_hash
            
        except ssl.SSLError as e:
            self.logger.error(f"Certificate verification error: {str(e)}")
            return False