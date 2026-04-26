import requests
import logging
from typing import Optional

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ServerMonitor:
    def __init__(self, url: str, timeout: int = 5):
        """
        Initialize the server monitor with URL and timeout parameters.
        
        Args:
            url: The URL of the server to monitor
            timeout: Maximum time in seconds to wait for response
        """
        if not url.startswith(('http://', 'https://')):
            raise ValueError("URL must start with http:// or https://")
        self.url = url
        self.timeout = timeout

    def check_server(self) -> bool:
        """
        Check the availability of the server.
        
        Returns:
            bool: True if server is available, False otherwise
        """
        try:
            response = requests.get(self.url, timeout=self.timeout)
            logger.info(f"Server {self.url} responded with status code: {response.status_code}")
            return response.status_code == 200
        except requests.RequestException as e:
            logger.error(f"Error checking server: {str(e)}")
            return False

    def monitor(self, interval: int = 300) -> Optional[bool]:
        """
        Monitor the server at specified interval.
        
        Args:
            interval: Time in seconds between checks
        
        Returns:
            Optional[bool]: True if server is available, False if server is unavailable,
                          None if monitoring was interrupted
        """
        try:
            while True:
                if self.check_server():
                    logger.info("Server is available")
                    return True
                logger.warning("Server is not available")
                # Wait for specified interval before next check
                import time
                time.sleep(interval)
        except KeyboardInterrupt:
            logger.info("Monitoring interrupted by user")
            return None

if __name__ == "__main__":
    # Example usage
    monitor = ServerMonitor("https://example.com")
    monitor.monitor(interval=60)