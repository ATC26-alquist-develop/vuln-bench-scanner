import requests
import logging
from typing import Optional
from urllib.parse import urlparse
import ssl

class SecureNetworkMonitor:
    def __init__(self, server_url: str, timeout: int = 5):
        """
        Initialize the network monitor with security controls.
        
        Args:
            server_url: The URL of the server to monitor
            timeout: Connection timeout in seconds
        """
        # Validate and sanitize URL
        parsed = urlparse(server_url)
        if not parsed.scheme or not parsed.netloc:
            raise ValueError("Invalid URL format")
        
        self.server_url = server_url
        self.timeout = timeout
        self._setup_logging()

    def _setup_logging(self) -> None:
        """Set up secure logging configuration."""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[logging.FileHandler('network_monitor.log'), logging.StreamHandler()]
        )

    def check_server(self) -> None:
        """
        Check server availability using HTTPS with certificate validation.
        """
        try:
            # Create a custom SSL context with strong security settings
            context = ssl.create_default_context()
            context.minimum_version = ssl.TLSVersion.TLSv1_2
            context.verify_mode = ssl.CERT_REQUIRED

            # Make HTTPS request with timeout and certificate validation
            with requests.Session() as session:
                session.mount('https://', requests.adapters.HTTPAdapter(
                    max_retries=3,
                    ssl_context=context
                ))

                response = session.get(
                    self.server_url,
                    timeout=self.timeout,
                    verify=True
                )

            if response.status_code == 200:
                logging.info(f"Server {self.server_url} is available")
            else:
                logging.warning(f"Server {self.server_url} returned status code {response.status_code}")

        except (requests.exceptions.RequestException, 
                ssl.SSLCertVerificationError) as e:
            logging.error(f"Error checking server: {str(e)}")

def main():
    try:
        # Example usage
        monitor = SecureNetworkMonitor("https://api.example.com")
        monitor.check_server()
    except Exception as e:
        logging.error(f"Initialization error: {str(e)}")

if __name__ == "__main__":
    main()