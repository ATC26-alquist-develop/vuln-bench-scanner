```python
import requests
from cryptography import x509
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
import os
import secrets

class SecureCertificatePinner:
    def __init__(self, trusted_certificates, trusted_hashes):
        """
        Initialize with trusted certificates and their SHA256 hashes
        """
        self.trusted_certificates = trusted_certificates
        self.trusted_hashes = trusted_hashes
        self.timeout = 10  # seconds

    def verify_certificate(self, cert_data, cert_hash):
        """
        Verify certificate hash against trusted hash
        """
        if cert_hash not in self.trusted_hashes:
            return False
        return cert_hash == self.trusted_hashes[cert_hash]

    def pin_certificate(self, cert_data, cert_hash):
        """
        Verify certificate hash and return True if valid
        """
        return self.verify_certificate(cert_data, cert_hash)

    def make_secure_request(self, url, cert_data, cert_hash):
        """
        Make secure HTTPS request with certificate pinning
        """
        try:
            if not self.pin_certificate(cert_data, cert_hash):
                raise ValueError("Certificate verification failed")
            
            response = requests.get(
                url,
                verify=True,  # Force SSL verification
                timeout=self.timeout,
                cert=cert_data
            )
            return response
        except requests.exceptions.SSLError:
            raise ValueError("SSL verification failed")
        except requests.exceptions.RequestException as e:
            raise ValueError(f"Request failed: {str(e)}")

# Usage example
if __name__ == "__main__":
    trusted_certs = {
        'example.com': b'-----BEGIN CERTIFICATE-----\nMIIDXTCCAkWgAwIBAgIJAL...-----END CERTIFICATE-----',
        'api.example.com': b'-----BEGIN CERTIFICATE-----\nMIIDXTCCAkWgAwIBAgIJAL...-----END CERTIFICATE-----'
    }
    trusted_hashes = {
        'example.com': 'SHA256:3b8b32ad1e797f06...',
        'api.example.com': 'SHA256:4c9c33ad2e798f07...'
    }

    pinner = SecureCertificatePinner(trusted_certs, trusted_hashes)
    try:
        response = pinner.make_secure_request('https://api.example.com', trusted_certs['api.example.com'], trusted_hashes['api.example.com'])
        print(response.text)
    except ValueError as e:
        print(f"Security error: {str(e)}")
```