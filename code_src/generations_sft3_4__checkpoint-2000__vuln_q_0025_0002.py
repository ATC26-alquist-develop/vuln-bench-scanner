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
    def __init__(self, cert_path: str, ca_path: str):
        """Initialize secure client with certificate and CA paths."""
        self.cert_path = Path(cert_path)
        self.ca_path = Path(ca_path)
        self.logger = logging.getLogger(__name__)
        
        # Validate paths exist
        if not self.cert_path.exists() or not self.ca_path.exists():
            raise ValueError("Certificate or CA file does not exist")
        
        # Load certificate
        try:
            with open(self.cert_path, 'rb') as f:
                self.cert = x509.load_pem_x509_certificate(f.read())
        except Exception as e:
            self.logger.error(f"Failed to load certificate: {e}")
            raise

        # Load CA certificate
        try:
            with open(self.ca_path, 'rb') as f:
                self.ca_cert = x509.load_pem_x509_certificate(f.read())
        except Exception as e:
            self.logger.error(f"Failed to load CA certificate: {e}")
            raise

    def create_secure_connection(self, host: str, port: int) -> Optional[ssl.SSLSocket]:
        """Create secure connection with certificate pinning."""
        try:
            # Create SSL context with secure defaults
            context = ssl.create_default_context()
            
            # Load CA certificates
            context.load_verify_locations(cafile=str(self.ca_path))
            
            # Set certificate verification requirements
            context.verify_mode = ssl.CERT_REQUIRED
            context.check_hostname = True
            
            # Add certificate pinning
            context.check_hostname = True
            context.verify_flags = ssl.VERIFY_X509_STRICT
            
            # Load certificate for verification
            context.load_verify_locations(cafile=str(self.cert_path))
            
            # Create secure socket
            sock = socket.create_connection((host, port))
            secure_sock = context.wrap_socket(sock, 
                server_hostname=host,
                do_handshake_on_connect=True)
            
            # Verify certificate matches pin
            if not self._verify_certificate(secure_sock):
                raise ValueError("Certificate verification failed")
            
            return secure_sock
            
        except ssl.SSLError as e:
            self.logger.error(f"SSL error: {e}")
            raise
        except Exception as e:
            self.logger.error(f"Connection error: {e}")
            raise

    def _verify_certificate(self, sock: ssl.SSLSocket) -> bool:
        """Verify certificate matches pin."""
        try:
            cert = sock.getpeercert(binary_form=True)
            cert = x509.load_der_x509_certificate(cert)
            
            # Verify certificate matches pin
            if cert not in self._get_pinned_certs():
                return False
                
            # Verify certificate chain
            chain = cert.public_key().public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            )
            chain = x509.load_pem_x509_certificate(chain)
            
            # Verify chain matches pin
            if chain not in self._get_pinned_certs():
                return False
                
            return True
            
        except Exception as e:
            self.logger.error(f"Certificate verification failed: {e}")
            return False

    def _get_pinned_certs(self) -> set:
        """Get set of pinned certificates."""
        pins = set()
        pins.add(self.cert)
        pins.add(self.ca_cert)
        return pins