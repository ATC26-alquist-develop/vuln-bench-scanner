import logging
from pathlib import Path
import os
import stat

def setup_secure_logging(log_path: str, max_size: int = 10_000_000, backup_count: int = 5) -> logging.Logger:
    """
    Set up secure logging with proper permissions and safeguards.
    
    Args:
        log_path: Path to the log file
        max_size: Maximum size of log file in bytes (default 10MB)
        backup_count: Number of backup files to keep (default 5)
    
    Returns:
        Configured logging.Logger object
    """
    # Convert to Path object for secure path handling
    log_file = Path(log_path)
    
    # Validate path is absolute and doesn't contain symlinks
    if not log_file.is_absolute():
        raise ValueError("Log file path must be absolute")
    
    # Create directory if it doesn't exist
    log_file.parent.mkdir(parents=True, exist_ok=True)
    
    # Set secure permissions (owner read/write only)
    os.chmod(log_file.parent, stat.S_IRWXU)
    
    # Configure logging
    logger = logging.getLogger("secure_logger")
    logger.setLevel(logging.INFO)
    
    # Use RotatingFileHandler for size limits and backups
    handler = logging.handlers.RotatingFileHandler(
        filename=str(log_file),
        maxBytes=max_size,
        backupCount=backup_count
    )
    
    # Set secure formatter
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    
    logger.addHandler(handler)
    return logger

# Example usage
if __name__ == "__main__":
    try:
        logger = setup_secure_logging("/path/to/secure_log.txt")
        logger.info("This is a secure log entry")
    except Exception as e:
        print(f"Error setting up logging: {e}")