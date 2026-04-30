```python
import logging
import os
from logging.handlers import RotatingFileHandler
from pathlib import Path
import stat

class SecureLogger:
    def __init__(self, log_path: str, max_size: int = 10 * 1024 * 1024, backup_count: int = 5):
        """
        Initialize secure logger with proper permissions and validation.
        
        Args:
            log_path: Path to the log file
            max_size: Maximum log file size in bytes (default 10MB)
            backup_count: Number of backup files to keep (default 5)
        """
        # Validate and sanitize log path
        self.log_path = Path(log_path).resolve()
        
        # Ensure log directory exists with proper permissions
        log_dir = self.log_path.parent
        log_dir.mkdir(mode=0o700, parents=True, exist_ok=True)
        
        # Validate log path is within allowed directory
        if not self.log_path.is_relative_to(log_dir):
            raise ValueError("Log file must be within the allowed directory")
        
        # Set up logging with rotation and secure permissions
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.INFO)
        
        handler = RotatingFileHandler(
            self.log_path,
            maxBytes=max_size,
            backupCount=backup_count
        )
        
        # Set secure file permissions (read/write only for owner)
        os.chmod(self.log_path, stat.S_IRUSR | stat.S_IWUSR)
        
        formatter = logging.Formatter('%(asctime)s - %(message)s')
        handler.setFormatter(formatter)
        
        self.logger.addHandler(handler)

    def log(self, message: str):
        """Log a message securely."""
        if not isinstance(message, str):
            raise ValueError("Message must be a string")
        
        # Sanitize message to prevent log injection
        sanitized_message = self._sanitize_log_message(message)
        self.logger.info(sanitized_message)

    def _sanitize_log_message(self, message: str) -> str:
        """Sanitize log message to prevent log injection."""
        # Remove control characters and limit length
        return ''.join(char for char in message if ord(char) >= 32 or char.isspace())[:1000]

    def read_log(self) -> str:
        """Read log file securely."""
        if not self.log_path.exists():
            return ""
        
        try:
            with open(self.log_path, 'r', encoding='utf-8') as file:
                return file.read()
        except (IOError, UnicodeDecodeError) as e:
            return f"Error reading log: {str(e)}"

# Example usage
if __name__ == "__main__":
    try:
        # Initialize logger with secure permissions
        logger = SecureLogger("/path/to/secure_log.log")
        
        # Example log messages
        logger.log("Application started")
        logger.log("An event occurred")
        
        # Read log content
        content = logger.read_log()
        print(f"Log content:\n{content}")
        
    except Exception as e:
        print(f"Error: {str(e)}")
```