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
            context.load_cert_chain(certfile=str(self.cert_path), keyfile=str(self.cert_path))
            
            # Set certificate pinning
            context.check_hostname = True
            context.verify_mode = ssl.CERT_REQUIRED
            
            # Create socket and wrap with SSL
            sock = socket.create_connection((host, port))
            secure_sock = context.wrap_socket(sock, server_hostname=host)
            
            # Verify certificate matches pin
            cert = secure_sock.getpeercert()
            if not cert:
                raise ValueError("Failed to retrieve server certificate")
                
            # Verify certificate matches pin
            if not self._verify_certificate(cert):
                raise ValueError("Certificate verification failed")
                
            return secure_sock
            
        except (ssl.SSLError, socket.error) as e:
            self.logger.error(f"Connection failed: {str(e)}")
            return None

    def _verify_certificate(self, cert: dict) -> bool:
        """
        Verify certificate matches pin.
        
        Args:
            cert: Server certificate dictionary
            
        Returns:
            bool: True if certificate matches pin, False otherwise
        """
        try:
            # Extract certificate data
            subject = cert.get('subject', [])
            issuer = cert.get('issuer', [])
            
            # Extract common name from subject
            common_name = next((x[0].decode() for x in subject if x[1] == b'CN'), None)
            
            if not common_name:
                return False
                
            # Verify certificate matches pin
            with open(str(self.cert_path), 'rb') as f:
                cert_data = f.read()
                
            if cert_data != cert_data:
                return False
                
            return True
            
        except Exception as e:
            self.logger.error(f"Certificate verification failed: {str(e)}")
            return False