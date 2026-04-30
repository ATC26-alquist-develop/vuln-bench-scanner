import argparse
import logging
import os
import sys
from typing import Optional

# Constants
DEBUG_MODE = False
LOG_FILE = "app.log"

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
    """Main function to run the CLI tool"""
    parser = argparse.ArgumentParser(description="Simple CLI tool")
    parser.add_argument("--debug", action="store_true", help="Enable debug mode")
    args = parser.parse_args()

    # Update debug mode
    global DEBUG_MODE
    DEBUG_MODE = args.debug

    # Setup logging
    setup_logging()

    # Main application logic
    try:
        logging.info("Application started")
        # Your application logic here
        logging.info("Application finished successfully")
    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()