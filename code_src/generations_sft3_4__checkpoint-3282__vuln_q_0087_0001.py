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
        Check server availability by making a GET request.
        
        Returns:
            bool: True if server is available, False otherwise
        """
        try:
            response = requests.get(self.base_url, timeout=self.timeout)
            return response.status_code == 200
        except requests.RequestException as e:
            self.logger.error(f"Error checking server: {str(e)}")
            return False

    def monitor(self, interval: int = 60) -> Optional[bool]:
        """
        Monitor server availability at specified interval.
        
        Args:
            interval: Time in seconds between checks
        
        Returns:
            Optional[bool]: True if server is available, False if server is down,
                           None if monitoring is interrupted
        """
        while True:
            try:
                result = self.check_server()
                if result:
                    self.logger.info("Server is available")
                else:
                    self.logger.warning("Server is not available")
                return result
            except Exception as e:
                self.logger.error(f"Monitoring error: {str(e)}")
                return None
            finally:
                # Prevent resource exhaustion
                if interval > 0:
                    import time
                    time.sleep(interval)

if __name__ == "__main__":
    # Example usage
    monitor = ServerMonitor("https://example.com")
    monitor.monitor(interval=30)