import logging
from pathlib import Path
import os

def setup_secure_logging(log_file_path: str, max_size: int = 10_000_000, backup_count: int = 5):
    """
    Set up secure logging with proper permissions and rotation.
    
    Args:
        log_file_path: Path to the log file
        max_size: Maximum size of each log file in bytes
        backup_count: Number of backup files to keep
    """
    # Convert to Path object for secure path handling
    log_path = Path(log_file_path)
    
    # Ensure log directory exists with proper permissions
    log_path.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
    
    # Set up logging configuration
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        filename=str(log_path),
        filemode='a'
    )
    
    # Set secure permissions for the log file
    os.chmod(log_path, 0o600)
    
    # Configure rotation
    file_handler = logging.handlers.RotatingFileHandler(
        filename=str(log_path),
        maxBytes=max_size,
        backupCount=backup_count
    )
    
    # Add handlers to root logger
    logging.getLogger('').addHandler(file_handler)
    
    return logging.getLogger(__name__)

# Example usage
if __name__ == '__main__':
    logger = setup_secure_logging('/path/to/secure/logfile.log')
    logger.info('This is a secure log message')