import ssl
import socket
from typing import Optional
from pathlib import Path
import logging
from datetime import datetime, timedelta

class SecureClient:
    def __init__(self, cert_path: str, pin_lifetime: timedelta = timedelta(days=30)):
        """
        Initialize secure client with certificate pinning
        
        Args:
            cert_path: Path to certificate file
            pin_lifetime: How long pin should be valid
        """
        self.cert_path = Path(cert_path)
        self._last_pinning = datetime.min
        self._pin_lifetime = pin_lifetime
        
        # Configure logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger('SecureClient')

    def _validate_cert(self, cert_data: bytes) -> bool:
        """
        Validate certificate matches pin
        
        Args:
            cert_data: Certificate data to validate
            
        Returns:
            bool: True if certificate matches pin
        """
        try:
            # Load certificate
            cert = ssl.PEM_cert_to_DER_cert(cert_data)
            
            # Get subject and issuer fingerprints
            subject_hash = self._hash_cert(cert, 'subject')
            issuer_hash = self._hash_cert(cert, 'issuer')
            
            # Check pin lifetime
            if datetime.now() - self._last_pinning > self._pin_lifetime:
                return False
                
            # Verify certificate matches pin
            return (subject_hash == self._get_cert_hash() and 
                   issuer_hash == self._get_cert_hash())
            
        except Exception as e:
            self.logger.error(f"Certificate validation error: {str(e)}")
            return False

    def _hash_cert(self, cert: bytes, hash_type: str) -> str:
        """
        Compute certificate hash
        
        Args:
            cert: Certificate data
            hash_type: Hash type ('subject' or 'issuer')
            
        Returns:
            str: Hash of certificate
        """
        if hash_type not in ['subject', 'issuer']:
            raise ValueError("Invalid hash type")
            
        # Get relevant section
        if hash_type == 'subject':
            cert_section = cert[4:4+72]  # Subject
        else:
            cert_section = cert[4+256:4+256+72]  # Issuer
            
        # Compute SHA-256 hash
        return ssl.DER_to_PEM(ssl.Hash(cert_section, 'sha256'))

    def _get_cert_hash(self) -> str:
        """
        Get stored certificate hash
        
        Returns:
            str: Certificate hash
        """
        try:
            with open(self.cert_path, 'rb') as f:
                return self._hash_cert(f.read(), 'subject')
        except Exception as e:
            self.logger.error(f"Error reading certificate: {str(e)}")
            return ''

    def connect(self, host: str, port: int) -> Optional[ssl.SSLSocket]:
        """
        Establish secure connection with certificate pinning
        
        Args:
            host: Host to connect to
            port: Port to connect on
            
        Returns:
            Optional[ssl.SSLSocket]: SSLSocket if connection successful
        """
        try:
            # Create secure context
            context = ssl.create_default_context()
            context.check_hostname = True
            context.verify_mode = ssl.CERT_REQUIRED
            
            # Add certificate pin
            context.load_verify_locations(cafile=str(self.cert_path))
            context.load_verify_locations(cadata=self._get_cert_hash().encode())
            
            # Create socket and wrap with SSL
            sock = socket.create_connection((host, port))
            return context.wrap_socket(sock, server_hostname=host)
            
        except Exception as e:
            self.logger.error(f"Connection error: {str(e)}")
            return None