import argparse
import logging
import os
import sys
from typing import Optional

# Constants
DEBUG_MODE = False
LOG_FILE = "debug.log"

def setup_logging() -> None:
    """Setup logging configuration"""
    logging.basicConfig(
        level=logging.DEBUG if DEBUG_MODE else logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(LOG_FILE),
            logging.StreamHandler(sys.stdout)
        ]
    )

def main() -> None:
    """Main function to handle command line arguments and execute the tool"""
    parser = argparse.ArgumentParser(description='Basic CLI tool')
    parser.add_argument('--debug', action='store_true', help='Enable debug mode')
    parser.add_argument('--log-file', type=str, default=LOG_FILE, help='Log file path')
    args = parser.parse_args()

    # Update log file path if provided
    if args.log_file:
        LOG_FILE = args.log_file

    setup_logging()

    # Main logic here
    logging.info("Starting the tool")
    # ... rest of the tool logic ...

if __name__ == '__main__':
    main()