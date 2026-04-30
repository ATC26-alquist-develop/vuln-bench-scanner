import os
import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
import stat

class SecureLogger:
    def __init__(self, log_file_path, max_size_bytes=10*1024*1024, backup_count=5):
        """Initialize secure logger with proper permissions and rotation."""
        self.log_file_path = Path(log_file_path).resolve()
        self.max_size_bytes = max_size_bytes
        self.backup_count = backup_count
        
        # Ensure log directory exists and has proper permissions
        log_dir = self.log_file_path.parent
        log_dir.mkdir(mode=0o700, parents=True, exist_ok=True)
        
        # Set secure permissions on log file
        self._setup_secure_permissions()
        
        # Configure secure logging
        self._setup_logging()

    def _setup_secure_permissions(self):
        """Set secure permissions on log file and directory."""
        os.chmod(self.log_file_path.parent, stat.S_IRWXU)
        os.chmod(self.log_file_path, stat.S_IRUSR | stat.S_IWUSR)

    def _setup_logging(self):
        """Configure secure logging with rotation."""
        handler = RotatingFileHandler(
            self.log_file_path,
            maxBytes=self.max_size_bytes,
            backupCount=self.backup_count
        )
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        
        logger = logging.getLogger('secure_logger')
        logger.setLevel(logging.INFO)
        logger.addHandler(handler)

    def log(self, message, level=logging.INFO):
        """Securely log a message."""
        logger = logging.getLogger('secure_logger')
        logger.log(level, message)

    def read_log(self):
        """Securely read log file contents."""
        try:
            with open(self.log_file_path, 'r') as f:
                return f.read()
        except IOError as e:
            logging.error(f"Error reading log file: {e}")
            return None

# Usage example
if __name__ == "__main__":
    secure_logger = SecureLogger("/path/to/secure_log.log")
    secure_logger.log("This is a secure log entry")
    content = secure_logger.read_log()
    if content:
        print(content)