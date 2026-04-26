import ssl
import socket
from typing import Optional
from pathlib import Path
import logging
from cryptography import x509
from cryptography.hazmat.backends import default_backend

class SecureClient:
    def __init__(self, cert_path: str, ca_path: str):
        """Initialize secure client with certificate and CA paths."""
        self.cert_path = Path(cert_path)
        self.ca_path = Path(ca_path)
        
        # Configure logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        
        # Validate paths
        if not self.cert_path.exists() or not self.ca_path.exists():
            raise ValueError("Certificate or CA file does not exist")
            
        # Load certificate
        try:
            with open(self.cert_path, 'rb') as f:
                self.cert = x509.load_pem_x509_certificate(
                    f.read(),
                    default_backend()
                )
        except Exception as e:
            self.logger.error(f"Failed to load certificate: {e}")
            raise

    def create_secure_connection(self, host: str, port: int) -> Optional[ssl.SSLSocket]:
        """Create secure connection with certificate pinning."""
        try:
            # Create SSL context with secure defaults
            context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
            
            # Load CA certificate
            with open(self.ca_path, 'rb') as f:
                context.load_verify_locations(cafile=f.read())
            
            # Set certificate verification
            context.verify_mode = ssl.CERT_REQUIRED
            
            # Add certificate pinning
            context.check_hostname = True
            context.verify_flags = ssl.VERIFY_X509_STRICT
            
            # Load certificate for pinning
            cert_pem = self.cert.public_bytes(
                encoding=ssl.PEM_ENCODING
            )
            
            # Add certificate pinning
            context.load_verify_locations(
                certfile=cert_pem,
                cadata=self.cert.public_bytes(
                    encoding=ssl.PEM_ENCODING
                )
            )
            
            # Create socket and wrap with SSL
            sock = socket.create_connection((host, port))
            secure_sock = context.wrap_socket(
                sock,
                server_hostname=host
            )
            
            # Verify certificate matches pin
            if not self.cert.verify(secure_sock.getpeercert(binary_form=True)):
                self.logger.error("Certificate verification failed")
                raise ssl.CertificateError("Certificate verification failed")
                
            return secure_sock
            
        except ssl.SSLError as e:
            self.logger.error(f"SSL error: {e}")
            raise
        except Exception as e:
            self.logger.error(f"Connection error: {e}")
            raise