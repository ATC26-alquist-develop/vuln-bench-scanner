import ftplib
import ssl
from urllib.parse import urlparse
import logging
from typing import Optional

class SecureFTPClient:
    def __init__(self, host: str, port: int = 21):
        """Initialize secure FTP client with proper validation."""
        # Validate host format
        parsed = urlparse(host)
        if not parsed.scheme or not parsed.netloc:
            raise ValueError("Invalid host format")
        
        self.host = parsed.netloc
        self.port = port
        self._connection: Optional[ftplib.FTP] = None
        
        # Configure logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

    def connect(self, username: str, password: str) -> bool:
        """Establish secure connection to FTP server."""
        try:
            # Create secure SSL context
            context = ssl.create_default_context()
            
            # Connect using SSL/TLS
            self._connection = ftplib.FTP_TLS(context=context)
            
            # Attempt connection
            self._connection.connect(
                self.host,
                port=self.port,
                timeout=10  # Set reasonable timeout
            )
            
            # Attempt TLS
            self._connection.starttls()
            
            # Login with provided credentials
            self._connection.login(username, password)
            
            # Set binary mode
            self._connection.binary()
            
            self.logger.info("Secure connection established")
            return True
            
        except (ftplib.all_errors, ssl.SSLError, ValueError) as e:
            self.logger.error(f"Connection failed: {str(e)}")
            return False

    def disconnect(self) -> None:
        """Safely disconnect from FTP server."""
        if self._connection:
            try:
                self._connection.quit()
                self._connection = None
                self.logger.info("Disconnected from FTP server")
            except Exception as e:
                self.logger.error(f"Error during disconnection: {str(e)}")

    def __enter__(self):
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.disconnect()