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
            
        # Ensure log directory exists with proper permissions
        self.log_file.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
        
        # Set up logging
        logging.basicConfig(
            filename=str(self.log_file),
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        
        # Set maximum file size
        self.max_size = max_size_mb * 1024 * 1024
        
        # Initialize lock for thread safety
        self.lock = Lock()
        
    def write_log(self, message: str) -> bool:
        """
        Safely write a message to the log file.
        
        Args:
            message: The message to write to the log
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            with self.lock:
                # Check file size
                if self.log_file.stat().st_size > self.max_size:
                    raise OSError("Log file size limit exceeded")
                
                # Write to file with proper permissions
                with open(self.log_file, 'a', encoding='utf-8') as f:
                    f.write(f"{message}\n")
                    os.chmod(self.log_file, 0o600)
                
                logging.info(message)
                return True
                
        except (IOError, OSError) as e:
            logging.error(f"Failed to write to log: {str(e)}")
            return False
            
    def read_log(self) -> Optional[str]:
        """
        Safely read the contents of the log file.
        
        Returns:
            Optional[str]: Contents of the log file or None if error occurs
        """
        try:
            with self.lock:
                if not self.log_file.exists():
                    return None
                with open(self.log_file, 'r', encoding='utf-8') as f:
                    return f.read()
        except (IOError, OSError) as e:
            logging.error(f"Failed to read log: {str(e)}")
            return None