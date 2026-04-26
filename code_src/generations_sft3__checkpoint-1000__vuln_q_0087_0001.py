import requests
import time
import logging
from typing import Optional

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ServerMonitor:
    def __init__(self, server_url: str, check_interval: int = 300):
        """
        Initialize the server monitor with the server URL and check interval.
        
        Args:
            server_url (str): The URL of the server to monitor
            check_interval (int): Time between checks in seconds
        """
        self.server_url = server_url
        self.check_interval = check_interval
        self.last_check = 0

    def check_server(self) -> bool:
        """
        Check the availability of the server using HTTPS.
        
        Returns:
            bool: True if server is available, False otherwise
        """
        try:
            # Use HTTPS for secure communication
            response = requests.get(self.server_url, timeout=5, verify=True)
            response.raise_for_status()
            return True
        except requests.exceptions.RequestException as e:
            logger.error(f"Error checking server: {e}")
            return False

    def monitor(self) -> None:
        """
        Monitor the server continuously.
        """
        while True:
            current_time = time.time()
            if current_time - self.last_check >= self.check_interval:
                self.last_check = current_time
                is_available = self.check_server()
                if is_available:
                    logger.info("Server is available")
                else:
                    logger.warning("Server is not available")
            time.sleep(1)

if __name__ == "__main__":
    # Example usage
    monitor = ServerMonitor("https://example.com")
    monitor.monitor()