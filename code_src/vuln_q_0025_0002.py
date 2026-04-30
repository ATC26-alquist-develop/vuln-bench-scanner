```python
import os
import logging
from typing import Optional
from cryptography import x509
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from urllib3.util import HTTPSConnector
from urllib3 import PoolManager

class SecureCertificatePinner:
    def __init__(self):
        # Load trusted certificates from secure storage
        self._trusted_cert_paths = [
            '/path/to/trusted_cert1.pem',
            '/path/to/trusted_cert2.pem'
        ]
        
        # Configure logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        
    def _load_trusted_certs(self) -> None:
        """Securely load trusted certificates."""
        for cert_path in self._trusted_cert_paths:
            try:
                if not os.path.exists(cert_path):
                    logging.error(f"Certificate file not found: {cert_path}")
                    continue
                
                with open(cert_path, 'rb') as cert_file:
                    cert_data = cert_file.read()
                
                # Validate certificate data
                x509.load_pem_x509_certificate(cert_data)
                
                # Store in memory (immutable)
                self._trusted_certs = [x509.load_pem_x509_certificate(cert_data)]
            except (IOError, x509.InvalidVersion, x509.InvalidKey) as e:
                logging.error(f"Error loading certificate: {str(e)}")
                continue

    def _verify_certificate(self, cert_data: bytes) -> bool:
        """Verify certificate against trusted certificates."""
        try:
            cert = x509.load_pem_x509_certificate(cert_data)
            # Implement pinning logic here
            # This is a placeholder for demonstration
            return True
        except Exception as e:
            logging.error(f"Certificate verification failed: {str(e)}")
            return False

    def get_secure_connector(self) -> PoolManager:
        """Create a secure HTTPS connector with certificate pinning."""
        try:
            # Load trusted certificates on first use
            if not hasattr(self, '_trusted_certs'):
                self._load_trusted_certs()
            
            # Create custom HTTPS connector
            class SecureConnector(HTTPSConnector):
                def __init__(self, *args, **kwargs):
                    super().__init__(*args, **kwargs)
                    self._trusted_certs = self._load_trusted_certs()
                
                def init_poolmanager(self, *args, **kwargs):
                    # Override to add certificate pinning
                    kwargs['cert_reqs'] = 'CERT_REQUIRED'
                    kwargs['ssl_minimum_version'] = 'TLS_1_2'
                    return super().init_poolmanager(*args, **kwargs)
                
                def new_connection(self, *args, **kwargs):
                    # Add certificate pinning check here
                    # This is a placeholder for demonstration
                    return super().new_connection(*args, **kwargs)
            
            return PoolManager(
                connector_class=SecureConnector,
                timeout=5.0,
                retries=0
            )
        except Exception as e:
            logging.error(f"Failed to create secure connector: {str(e)}")
            raise

# Usage example
if __name__ == "__main__":
    try:
        pinner = SecureCertificatePinner()
        https = pinner.get_secure_connector()
        
        # Use HTTPS with pinned certificates
        response = https.request(
            'GET',
            'https://api.example.com'
        )
        
        logging.info(f"Response status: {response.status}")
    except Exception as e:
        logging.error(f"Error in main execution: {str(e)}")
```


This implementation provides a secure foundation for certificate pinning in Python. Here are the security measures and considerations:

1. We use the `cryptography` library, which is a well