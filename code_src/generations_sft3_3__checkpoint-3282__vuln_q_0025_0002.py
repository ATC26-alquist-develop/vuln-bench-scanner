import ssl
import socket
from typing import Optional
from pathlib import Path
import logging
from datetime import datetime, timedelta

class SecureClient:
    def __init__(self, cert_path: str, pin_lifetime: int = 30):
        """
        Initialize secure client with certificate pinning
        
        Args:
            cert_path: Path to certificate file
            pin_lifetime: Maximum age of certificate pin in days
        """
        self.cert_path = Path(cert_path)
        self.pin_lifetime = pin_lifetime
        self._last_pinning = datetime.min
        self._pinned_cert_hash: Optional[str] = None
        
        # Configure logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger('SecureClient')

    def _validate_cert(self, cert_hash: str) -> bool:
        """Validate certificate hash against stored pin"""
        if not self._pinned_cert_hash:
            return False
            
        # Check if pin is expired
        if datetime.now() - self._last_pinning > timedelta(days=self.pin_lifetime):
            self._pinned_cert_hash = None
            return False
            
        return cert_hash == self._pinned_cert_hash

    def _get_cert_hash(self) -> Optional[str]:
        """Get certificate hash from file"""
        try:
            with open(self.cert_path, 'rb') as f:
                cert_data = f.read()
                return cert_data[:20].hex()  # Get first 20 bytes as hash
        except Exception as e:
            self.logger.error(f"Error reading certificate: {e}")
            return None

    def connect(self, host: str, port: int) -> ssl.SSLSocket:
        """Establish secure connection with certificate pinning"""
        try:
            # Get certificate hash
            cert_hash = self._get_cert_hash()
            if not cert_hash:
                raise ValueError("Failed to get certificate hash")

            # Validate certificate
            if not self._validate_cert(cert_hash):
                raise ValueError("Certificate validation failed")

            # Create secure context
            context = ssl.create_default_context()
            context.check_hostname = True
            context.verify_mode = ssl.CERT_REQUIRED

            # Add certificate pinning
            context.options |= ssl.OP_NO_SSLv2
            context.options |= ssl.OP_NO_SSLv3
            context.options |= ssl.OP_NO_TLSv1
            context.options |= ssl.OP_NO_TLSv1_1
            context.load_verify_locations(cafile=str(self.cert_path))
            context.load_verify_locations(cadata=cert_hash.encode())

            # Establish connection
            sock = socket.create_connection((host, port))
            secure_sock = context.wrap_socket(sock, server_hostname=host)
            
            self._last_pinning = datetime.now()
            self._pinned_cert_hash = cert_hash
            
            return secure_sock

        except Exception as e:
            self.logger.error(f"Connection failed: {e}")
            raise