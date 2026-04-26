import requests
from urllib.parse import urlparse
import ssl
import certifi
import logging
from typing import Optional

class SecureClient:
    def __init__(self, certificate_pinning: Optional[dict] = None):
        """
        Initialize secure client with optional certificate pinning
        """
        self.session = requests.Session()
        self.session.verify = certifi.where()
        
        # Configure secure defaults
        self.session.mount('https://', requests.adapters.HTTPAdapter(
            max_retries=3,
            pool_connections=10,
            pool_maxsize=10
        ))
        
        # Setup logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        
        # Certificate pinning
        if certificate_pinning:
            self._setup_certificate_pinning(certificate_pinning)

    def _setup_certificate_pinning(self, certificate_pinning: dict):
        """
        Configure certificate pinning
        """
        # Validate certificate pinning data
        if not isinstance(certificate_pinning, dict):
            raise ValueError("Certificate pinning must be a dictionary")
            
        # Store pinning data
        self._pinning_data = certificate_pinning
        
        # Configure SSL context
        self.session.mount('https://', requests.adapters.HTTPAdapter(
            ssl_context=self._create_ssl_context()
        ))

    def _create_ssl_context(self) -> ssl.SSLContext:
        """
        Create custom SSL context with pinning
        """
        context = ssl.create_default_context(cafile=certifi.where())
        
        # Add pinning
        if self._pinning_data:
            for domain, cert_hash in self._pinning_data.items():
                if not isinstance(domain, str) or not isinstance(cert_hash, str):
                    raise ValueError("Invalid pinning data format")
                context.set_certs([domain, cert_hash])
                
        return context

    def _validate_url(self, url: str) -> bool:
        """
        Validate URL format
        """
        try:
            result = urlparse(url)
            return all([result.scheme, result.netloc])
        except Exception:
            return False

    def make_secure_request(self, url: str, method: str = 'GET', 
                           data: Optional[dict] = None, 
                           headers: Optional[dict] = None) -> requests.Response:
        """
        Make secure HTTPS request with certificate pinning
        """
        # Validate URL
        if not self._validate_url(url):
            raise ValueError("Invalid URL format")

        # Configure request
        request = requests.Request(
            method=method,
            url=url,
            headers=headers or {},
            data=data
        )
        
        # Make request with security settings
        return self.session.send(
            request.prepare(),
            verify=True,
            timeout=30,
            allow_redirects=False
        )