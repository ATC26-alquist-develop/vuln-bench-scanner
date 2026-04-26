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
        self._setup_logging()
        self._setup_context()

    def _setup_logging(self) -> None:
        """Configure secure logging."""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )

    def _setup_context(self) -> None:
        """Create secure SSL context with certificate pinning."""
        self.context = ssl.create_default_context()
        
        # Load CA certificates
        with open(self.ca_path, 'rb') as ca_file:
            self.context.load_verify_locations(cafile=ca_file)
        
        # Load client certificate
        with open(self.cert_path, 'rb') as cert_file:
            cert_data = cert_file.read()
            try:
                cert = x509.load_pem_x509_certificate(cert_data)
            except ValueError as e:
                logging.error(f"Invalid certificate: {e}")
                raise

        # Get certificate hash
        cert_hash = cert.fingerprint(hashes.SHA256()).hex()

        # Add certificate pinning
        self.context.check_hostname = True
        self.context.verify_mode = ssl.CERT_REQUIRED
        self.context.load_verify_locations(cafile=self.ca_path)
        self.context.load_cert_chain(certfile=self.cert_path, keyfile='')
        self.context.verify_flags = ssl.VERIFY_CERTIFICATE
        self.context.options |= ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1

    def connect(self, host: str, port: int) -> ssl.SSLSocket:
        """Establish secure connection with certificate pinning."""
        try:
            sock = socket.create_connection((host, port))
            secure_sock = self.context.wrap_socket(
                sock,
                server_hostname=host
            )
            logging.info(f"Successfully connected to {host}:{port}")
            return secure_sock
        except (ssl.SSLError, socket.error) as e:
            logging.error(f"Connection failed: {e}")
            raise

    def verify_hostname(self, host: str) -> bool:
        """Verify hostname matches certificate."""
        try:
            cert = self.context.get_server_certificate((host, 443))
            cert_obj = x509.load_pem_x509_certificate(cert.encode())
            return cert_obj.subject.get_attributes_for_oid(NameOID.COMMON_NAME)[0].value == host
        except Exception as e:
            logging.error(f"Hostname verification failed: {e}")
            return False