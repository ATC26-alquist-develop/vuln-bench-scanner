import requests
import logging
from typing import Optional

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ServerMonitor:
    def __init__(self, url: str, timeout: int = 5):
        """
        Initialize the server monitor with URL and timeout.
        
        Args:
            url: The URL of the server to monitor
            timeout: Request timeout in seconds
        """
        if not url.startswith(('http://', 'https://')):
            raise ValueError("URL must start with http:// or https://")
        self.url = url
        self.timeout = timeout

    def check_server(self) -> bool:
        """
        Check if the server is available.
        
        Returns:
            bool: True if server is available, False otherwise
        """
        try:
            response = requests.get(self.url, timeout=self.timeout)
            return response.status_code == 200
        except requests.RequestException as e:
            logger.error(f"Error checking server: {e}")
            return False

def main():
    # Example usage
    try:
        monitor = ServerMonitor("https://example.com")
        is_available = monitor.check_server()
        print(f"Server is {'available' if is_available else 'not available'}")
    except ValueError as e:
        logger.error(f"Invalid input: {e}")

if __name__ == "__main__":
    main()