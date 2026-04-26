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
        self._setup_logging()
        
    def _setup_logging(self) -> None:
        """Configure secure logging."""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        
    def _validate_cert(self, cert_data: bytes) -> bool:
        """Validate certificate using strict pinning."""
        try:
            # Load certificate from file
            with open(self.cert_path, 'rb') as f:
                cert = f.read()
            
            # Verify certificate matches our pin
            return cert == cert_data
            
        except Exception as e:
            logging.error(f"Certificate validation error: {e}")
            return False
            
    def _create_secure_context(self) -> ssl.SSLContext:
        """Create secure SSL context with pinning."""
        context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
        
        # Load CA certificates
        context.load_verify_locations(cafile=str(self.ca_path))
        
        # Set certificate pinning
        context.verify_mode = ssl.CERT_REQUIRED
        context.check_hostname = True
        
        # Add certificate pin
        context.load_verify_locations(cafile=str(self.cert_path))
        context.verify_flags = ssl.VERIFY_X509_STRICT
        
        return context
        
    def connect(self, host: str, port: int) -> Optional[ssl.SSLSocket]:
        """Establish secure connection with certificate pinning."""
        try:
            # Create secure context
            context = self._create_secure_context()
            
            # Create socket
            sock = socket.create_connection((host, port))
            
            # Wrap socket with SSL
            secure_sock = context.wrap_socket(
                sock,
                server_hostname=host
            )
            
            # Verify certificate
            cert_data = secure_sock.getpeercert(binary_form=True)
            if not self._validate_cert(cert_data):
                logging.error("Certificate validation failed")
                return None
                
            logging.info(f"Secure connection established with {host}")
            return secure_sock
            
        except ssl.SSLError as e:
            logging.error(f"SSL error: {e}")
            return None
        except socket.error as e:
            logging.error(f"Socket error: {e}")
            return None
        except Exception as e:
            logging.error(f"Unexpected error: {e}")
            return None