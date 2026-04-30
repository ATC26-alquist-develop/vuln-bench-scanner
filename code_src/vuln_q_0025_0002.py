import ssl
import certifi
import requests
from urllib.parse import urlparse
import logging
from typing import Optional

class SecureClient:
    def __init__(self, 
                 certificate_path: Optional[str] = None,
                 verify: bool = True,
                 timeout: int = 30):
        """
        Initialize secure client with optional certificate pinning
        
        Args:
            certificate_path: Path to custom certificate file (optional)
            verify: Whether to verify SSL certificates
            timeout: Request timeout in seconds
        """
        # Configure logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        
        # Set up SSL context
        self.ssl_context = ssl.create_default_context(cafile=certifi.where())
        
        # Configure certificate pinning if provided
        if certificate_path:
            self._setup_certificate_pinning(certificate_path)
            
        # Configure timeout
        self.timeout = timeout
        
        # Configure requests session
        self.session = requests.Session()
        self.session.verify = verify
        self.session.mount('https://', 
                           requests.adapters.HTTPAdapter(
                               max_retries=3,
                               pool_connections=10,
                               pool_maxsize=10
                           ))

    def _setup_certificate_pinning(self, certificate_path: str) -> None:
        """
        Setup certificate pinning
        
        Args:
            certificate_path: Path to custom certificate file
        """
        try:
            with open(certificate_path, 'rb') as cert_file:
                cert_data = cert_file.read()
            
            # Create custom certificate context
            self.ssl_context.load_cert_chain(certfile=certificate_path)
            self.ssl_context.verify_mode = ssl.CERT_REQUIRED
            self.ssl_context.check_hostname = True
            self.ssl_context.verify_flags = ssl.VERIFY_X509_STRICT
            
            self.logger.info("Certificate pinning configured successfully")
        except Exception as e:
            self.logger.error(f"Certificate pinning setup failed: {str(e)}")
            raise

    def _validate_url(self, url: str) -> bool:
        """
        Validate URL format
        
        Args:
            url: URL to validate
            
        Returns:
            bool: True if URL is valid, False otherwise
        """
        try:
            result = urlparse(url)
            return all([result.scheme, result.netloc])
        except Exception:
            return False

    def make_request(self, url: str, method: str = 'GET', 
                    data: Optional[dict] = None, 
                    headers: Optional[dict] = None) -> requests.Response:
        """
        Make secure HTTPS request
        
        Args:
            url: URL to request
            method: HTTP method (GET, POST, etc.)
            data: Request data (for POST/PUT)
            headers: Request headers
            
        Returns:
            Response: HTTP response object
            
        Raises:
            ValueError: If URL is invalid
            ssl.SSLCertVerificationError: If SSL verification fails
            requests.exceptions.RequestException: For other request errors
        """
        # Validate URL
        if not self._validate_url(url):
            raise ValueError("Invalid URL format")

        try:
            # Make request with SSL verification
            response = self.session.request(
                method=method.upper(),
                url=url,
                data=data,
                headers=headers,
                timeout=self.timeout,
                verify=True
            )
            return response
        except requests.exceptions.SSLCertVerificationError as e:
            self.logger.error(f"SSL certificate verification failed: {str(e)}")
            raise
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Request failed: {str(e)}")
            raise