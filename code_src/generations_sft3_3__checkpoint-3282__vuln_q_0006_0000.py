import logging
import os
from pathlib import Path

def setup_secure_logging(log_file_path: str) -> None:
    """
    Set up secure logging with proper permissions.
    
    Args:
        log_file_path: Path to the log file
    """
    try:
        # Create directory if it doesn't exist
        log_dir = os.path.dirname(log_file_path)
        Path(log_dir).mkdir(parents=True, exist_ok=True)
        
        # Set secure permissions (only owner can read/write)
        os.chmod(log_dir, 0o700)
        
        # Configure logging
        logging.basicConfig(
            filename=log_file_path,
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        # Set secure permissions for the log file
        os.chmod(log_file_path, 0o600)
        
        # Test logging
        logging.info("This is a test log entry")
        
    except Exception as e:
        logging.error(f"Failed to setup logging: {str(e)}")
        raise

# Example usage
if __name__ == "__main__":
    log_file = "/path/to/your/logfile.log"
    setup_secure_logging(log_file)