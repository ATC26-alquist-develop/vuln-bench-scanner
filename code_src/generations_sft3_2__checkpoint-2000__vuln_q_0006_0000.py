import os
import logging
from pathlib import Path
from threading import Lock
from typing import Optional

class SecureSharedLog:
    def __init__(self, log_file_path: str, max_size_mb: int = 10):
        """
        Initialize a secure shared log file with proper access controls.
        
        Args:
            log_file_path: Path to the log file
            max_size_mb: Maximum size of the log file in MB
        """
        # Convert to absolute path and validate
        self.log_file = Path(log_file_path).resolve()
        if not self.log_file.parent.exists():
            raise ValueError("Log directory does not exist")
            
        # Ensure log directory exists
        self.log_file.parent.mkdir(parents=True, exist_ok=True)
        
        # Set maximum file size
        self.max_size = max_size_mb * 1024 * 1024
        
        # Create log file with secure permissions
        self._create_log_file()
        
        # Set up logging
        logging.basicConfig(
            filename=str(self.log_file),
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        
        # Thread-safe logging
        self.lock = Lock()
        
    def _create_log_file(self) -> None:
        """Create log file with secure permissions."""
        # Set restrictive permissions (owner read/write only)
        os.chmod(self.log_file, 0o600)
        
        # Ensure file size is within limits
        if self.log_file.stat().st_size > self.max_size:
            raise ValueError("Log file exceeds maximum allowed size")
            
    def write_log(self, message: str) -> None:
        """
        Write a message to the log file with proper synchronization.
        
        Args:
            message: The message to write to the log
        """
        with self.lock:
            try:
                with open(self.log_file, 'a', encoding='utf-8') as f:
                    f.write(f"{message}\n")
                    f.flush()
                    os.fsync(f.fileno())
            except IOError as e:
                logging.error(f"Failed to write to log file: {e}")
                raise
                
    def read_log(self) -> Optional[str]:
        """
        Read the last log entry.
        
        Returns:
            The last log entry or None if no entries exist
        """
        try:
            with open(self.log_file, 'r', encoding='utf-8') as f:
                return f.read().strip()
        except IOError as e:
            logging.error(f"Failed to read log file: {e}")
            return None