import logging
from pathlib import Path
from logging.handlers import RotatingFileHandler
import os

def setup_secure_logging(log_file_path: str, max_size: int = 10_000_000, backup_count: int = 5):
    """
    Set up secure logging with proper access controls.
    
    Args:
        log_file_path: Path to the log file
        max_size: Maximum size of log file in bytes
        backup_count: Number of backup files to keep
    """
    # Convert to absolute path and validate
    log_path = Path(log_file_path).resolve()
    if not log_path.parent.exists():
        raise ValueError("Log directory does not exist")
    
    # Create directory if it doesn't exist
    log_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Set secure permissions (read/write only for owner)
    os.chmod(log_path.parent, 0o700)
    os.chmod(log_path, 0o600)
    
    # Configure logging
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    
    # Use RotatingFileHandler to prevent excessive disk usage
    handler = RotatingFileHandler(
        filename=str(log_path),
        maxBytes=max_size,
        backupCount=backup_count
    )
    
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    
    logger.addHandler(handler)
    
    return logger

# Example usage
if __name__ == "__main__":
    try:
        logger = setup_secure_logging("/path/to/logfile.log")
        logger.info("This is a secure log message")
    except Exception as e:
        print(f"Error setting up logging: {e}")