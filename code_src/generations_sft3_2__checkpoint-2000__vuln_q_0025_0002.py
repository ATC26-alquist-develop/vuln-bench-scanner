```python
import ssl
import socket
from typing import Optional
from pathlib import Path
import logging
from cryptography import x509
from cryptography.hazmat.primitives import hashes
from cryptography.x509.oid import NameOID
from cryptography.exceptions import InvalidSignature

class SecureClient:
    def __init__(self, cert_path: str, ca_path: Optional[str] = None):
        """Initialize secure client with certificate and optional CA certificate."""
        self.cert_path = Path(cert_path).resolve()
        self.ca_path = ca_path and Path(ca_path).resolve() or None
        
        # Validate certificate file exists and is readable
        if not self.cert_path.is_file():
            raise ValueError("Certificate file does not exist")
        
        # Configure logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

    def create_secure_connection(self, hostname: str, port: int = 443) -> ssl.SSLSocket:
        """Create a secure SSL connection with certificate pinning."""
        try:
            # Create SSL context with secure defaults
            context = ssl.create_default_context()
            
            # Load certificate
            with open(self.cert_path, 'rb') as cert_file:
                cert_data = cert_file.read()
            
            # Parse certificate
            cert = x509.load_pem_x509_certificate(cert_data)
            
            # Verify certificate
            if not self._verify_certificate(cert):
                raise ValueError("Certificate verification failed")
            
            # Load CA certificate if provided
            ca_cert = None
            if self.ca_path:
                with open(self.ca_path, 'rb') as ca_file:
                    ca_cert_data = ca_file.read()
                ca_cert = x509.load_pem_x509_certificate(ca_cert_data)
            
            # Configure SSL context
            context.load_verify_locations(cafile=self.ca_path)
            context.verify_mode = ssl.CERT_REQUIRED
            context.check_hostname = True
            context.load_cert_chain(certfile=self.cert_path, keyfile=None)
            
            # Create socket and wrap with SSL
            sock = socket.create_connection((hostname, port))
            secure_sock = context.wrap_socket(sock, server_hostname=hostname)
            
            # Verify certificate matches our certificate
            if not self._verify_cert_matches(self.cert_path, secure_sock):
                raise ValueError("Certificate mismatch")
            
            return secure_sock

        except ssl.SSLError as e:
            self.logger.error(f"SSL error occurred: {str(e)}")
            raise
        except Exception as e:
            self.logger.error(f"Error occurred: {str(e)}")
            raise

    def _verify_certificate(self, cert: x509.X509) -> bool:
        """Verify certificate is valid and matches our certificate."""
        try:
            # Verify basic validity
            if cert.not_valid_before > cert.not_valid_after:
                return False
            
            # Verify common name matches hostname
            if cert.subject.get_attributes_for_oid(NameOID.COMMON_NAME)[0].value != socket.gethostname():
                return False
                
            # Verify certificate matches our certificate
            if not self._verify_cert_matches(self.cert_path, cert):
                return False
                
            return True
            
        except Exception as e:
            self.logger.error(f"Certificate verification failed: {str(e)}")
            return False

    def _verify_cert_matches(self, cert_path: Path, cert: x509.X509) -> bool:
        """Verify certificate matches the provided certificate."""
        try:
            with open(cert_path, 'rb') as cert_file:
                stored_cert_data = cert_file.read()
            stored_cert = x509.load_pem_x509_certificate(stored_cert_data)
            
            # Verify signature
            stored_cert_public_key = stored_cert.public_key()
            cert_public_key = cert.public_key()