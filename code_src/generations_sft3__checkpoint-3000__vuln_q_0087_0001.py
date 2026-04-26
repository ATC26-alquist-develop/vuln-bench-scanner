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
        self.base_url = base_url
        self.timeout = timeout
        self.logger = logging.getLogger(__name__)
        
        # Validate URL
        parsed_url = urlparse(base_url)
        if not all([parsed_url.scheme, parsed_url.netloc]):
            raise ValueError("Invalid URL format")
        if parsed_url.scheme not in ['http', 'https']:
            raise ValueError("Only HTTP(S) protocols are supported")

    def check_server(self) -> bool:
        """
        Check if the server is available.
        
        Returns:
            bool: True if server is available, False otherwise
        """
        try:
            response = requests.get(
                self.base_url,
                timeout=self.timeout,
                verify=True  # Verify SSL certificates
            )
            return response.status_code == 200
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Error checking server: {str(e)}")
            return False

    def monitor(self, interval: int = 60) -> Optional[bool]:
        """
        Monitor the server at specified interval.
        
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
            except KeyboardInterrupt:
                self.logger.info("Monitoring interrupted by user")
                return None
            except Exception as e:
                self.logger.error(f"Unexpected error during monitoring: {str(e)}")
                return None
            finally:
                import time
                time.sleep(interval)

if __name__ == "__main__":
    # Example usage
    monitor = ServerMonitor("https://example.com")
    monitor.monitor(interval=60)