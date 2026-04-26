import requests
import logging
from typing import Optional
from urllib.parse import urlparse

class ServerMonitor:
    def __init__(self, base_url: str, timeout: int = 5):
        """
        Initialize the server monitor with base URL and timeout.
        
        Args:
            base_url: Base URL of the server to monitor
            timeout: Request timeout in seconds
        """
        # Validate URL format
        if not self._is_valid_url(base_url):
            raise ValueError("Invalid URL format")
        
        self.base_url = base_url
        self.timeout = timeout
        self.logger = logging.getLogger(__name__)

    def _is_valid_url(self, url: str) -> bool:
        """Validate URL format and scheme."""
        try:
            result = urlparse(url)
            return all([result.scheme, result.netloc]) and result.scheme in ['http', 'https']
        except Exception:
            return False

    def check_server(self) -> bool:
        """
        Check server availability using GET request.
        
        Returns:
            bool: True if server is available, False otherwise
        """
        try:
            response = requests.get(self.base_url, timeout=self.timeout)
            return response.status_code == 200
        except requests.RequestException as e:
            self.logger.error(f"Error checking server: {str(e)}")
            return False

    def get_server_status(self) -> Optional[str]:
        """
        Get server status as a human-readable string.
        
        Returns:
            Optional[str]: Status message or None if server is unavailable
        """
        if self.check_server():
            return "Server is available"
        else:
            return "Server is unavailable"

if __name__ == "__main__":
    # Example usage
    monitor = ServerMonitor("https://example.com")
    print(monitor.get_server_status())