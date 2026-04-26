import requests
import logging
from typing import Optional
from urllib.parse import urlparse

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ServerMonitor:
    def __init__(self, base_url: str, timeout: int = 5):
        """
        Initialize the server monitor with base URL and timeout.
        
        Args:
            base_url: The base URL of the server to monitor
            timeout: Request timeout in seconds
        """
        self.base_url = self._validate_url(base_url)
        self.timeout = timeout

    def _validate_url(self, url: str) -> str:
        """Validate and return the URL."""
        try:
            result = urlparse(url)
            if not all([result.scheme, result.netloc]):
                raise ValueError("Invalid URL format")
            if result.scheme not in ['http', 'https']:
                raise ValueError("Only HTTP(S) protocols are allowed")
            return url
        except Exception as e:
            logger.error(f"URL validation error: {e}")
            raise ValueError(f"Invalid URL: {url}")

    def check_server(self) -> bool:
        """
        Check the availability of the server.
        
        Returns:
            bool: True if server is available, False otherwise
        """
        try:
            response = requests.get(self.base_url, timeout=self.timeout)
            return response.status_code == 200
        except requests.RequestException as e:
            logger.error(f"Error checking server: {e}")
            return False

def main():
    try:
        monitor = ServerMonitor("https://example.com")
        is_available = monitor.check_server()
        print(f"Server is {'available' if is_available else 'not available'}")
    except ValueError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()