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
            raise ValueError("Certificate or CA file not found")
        
        # Load certificate
        try:
            with open(self.cert_path, 'rb') as f:
                self.cert = x509.load_pem_x509_certificate(
                    f.read(),
                    default_backend()
                )
        except Exception as e:
            self.logger.error(f"Certificate loading error: {e}")
            raise

    def create_secure_connection(self, hostname: str, port: int = 443) -> Optional[ssl.SSLSocket]:
        """Create secure connection with certificate pinning."""
        try:
            # Create secure context
            context = ssl.create_default_context(
                purpose=ssl.Purpose.SERVER_AUTH,
                cafile=str(self.ca_path)
            )
            
            # Add certificate pinning
            context.check_hostname = True
            context.verify_mode = ssl.CERT_REQUIRED
            
            # Load certificate for pinning
            context.load_verify_locations(cafile=str(self.ca_path))
            context.load_cert_chain(certfile=str(self.cert_path))
            
            # Create socket and wrap with SSL
            sock = socket.create_connection((hostname, port))
            secure_sock = context.wrap_socket(
                sock,
                server_hostname=hostname
            )
            
            # Verify certificate matches pin
            if not self._verify_cert_matches_pinning(secure_sock):
                raise ssl.CertificateError("Certificate verification failed")
            
            return secure_sock
            
        except ssl.SSLError as e:
            self.logger.error(f"SSL error: {e}")
            raise
        except socket.error as e:
            self.logger.error(f"Socket error: {e}")
            raise
        except Exception as e:
            self.logger.error(f"Unexpected error: {e}")
            raise

    def _verify_cert_matches_pinning(self, sock: ssl.SSLSocket) -> bool:
        """Verify server certificate matches pin."""
        cert = sock.getpeercert(binary_form=True)
        cert_obj = x509.load_der_x509_certificate(cert, default_backend())
        
        # Verify common name matches hostname
        if cert_obj.subject.get_attributes_for_oid(x509.NameOID.COMMON_NAME)[0].value != sock.getpeername()[0]:
            return False
            
        # Verify certificate matches pin
        try:
            cert_hash = cert_obj.fingerprint(
                algorithm=ssl.FingerprintAlgorithm.SHA256
            ).hex()
            cert_hash = cert_hash[:8]  # Use first 8 chars as hash
            
            cert_file = self.cert_path.read_bytes()
            cert_hash_from_file = cert_file[:8].hex()
            
            return cert_hash == cert_hash_from_file
        except Exception:
            return False

    def __del__(self):
        """Cleanup resources."""
        self.logger.info("Cleaning up secure client resources")