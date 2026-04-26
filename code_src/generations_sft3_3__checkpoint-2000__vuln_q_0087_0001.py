import requests
import logging
from typing import Optional
from urllib.parse import urlparse
import ssl

class SecureServerMonitor:
    def __init__(self, server_url: str, timeout: int = 5, max_retries: int = 3):
        """
        Initialize the server monitor with security controls
        
        Args:
            server_url: The URL of the server to monitor
            timeout: Request timeout in seconds
            max_retries: Maximum number of retry attempts
        """
        # Validate URL
        parsed_url = urlparse(server_url)
        if not all([parsed_url.scheme, parsed_url.netloc]):
            raise ValueError("Invalid server URL")
        
        self.server_url = server_url
        self.timeout = timeout
        self.max_retries = max_retries
        self.session = requests.Session()
        
        # Configure logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

    def _make_request(self, method: str, **kwargs) -> Optional[requests.Response]:
        """
        Make a secure HTTP request with security controls
        
        Args:
            method: HTTP method (GET, POST, etc.)
            kwargs: Additional request parameters
            
        Returns:
            Response object if successful, None if failed
        """
        try:
            # Configure SSL context
            ssl_context = ssl.create_default_context()
            ssl_context.check_hostname = True
            ssl_context.verify_mode = ssl.CERT_REQUIRED

            # Make request with security controls
            response = self.session.request(
                method,
                self.server_url,
                timeout=self.timeout,
                verify=True,  # Enforce SSL certificate verification
                **kwargs
            )
            
            # Log successful request
            self.logger.info(f"Request successful: {method} {self.server_url}")
            return response
            
        except requests.exceptions.RequestException as e:
            # Log failed request
            self.logger.error(f"Request failed: {method} {self.server_url} - {str(e)}")
            return None

    def check_server_availability(self) -> bool:
        """
        Check if the server is available
        
        Returns:
            True if server is available, False otherwise
        """
        for attempt in range(self.max_retries):
            response = self._make_request('HEAD')
            if response is not None:
                return True
            self.logger.warning(f"Attempt {attempt + 1} failed. Retrying...")
            
        return False

    def __del__(self):
        """
        Ensure proper cleanup of resources
        """
        self.session.close()

# Example usage
if __name__ == "__main__":
    monitor = SecureServerMonitor("https://example.com")
    if monitor.check_server_availability():
        print("Server is available")
    else:
        print("Server is not available")