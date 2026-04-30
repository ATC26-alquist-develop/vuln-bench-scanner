import argparse
import logging
import os
import sys
from typing import Optional

# Secure debug mode constant
DEBUG_MODE: bool = False

def setup_logging(debug: bool = False) -> None:
    """
    Set up logging configuration securely.
    
    Args:
        debug: Whether to enable debug-level logging
    """
    log_level = logging.DEBUG if debug else logging.INFO
    log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    logging.basicConfig(
        level=log_level,
        format=log_format,
        handlers=[
            logging.StreamHandler(sys.stdout)
        ]
    )

def validate_input(input_value: str) -> str:
    """
    Validate and sanitize input to prevent injection attacks.
    
    Args:
        input_value: The input string to validate
        
    Returns:
        Sanitized input string
        
    Raises:
        ValueError: If input validation fails
    """
    # Remove any potentially dangerous characters
    sanitized = ''.join(c for c in input_value if c.isalnum() or c.isspace())
    
    if not sanitized:
        raise ValueError("Input cannot be empty after sanitization")
        
    return sanitized

def main() -> None:
    """
    Main function for the CLI tool.
    
    Parses command-line arguments, sets up logging, and performs the main operation.
    """
    parser = argparse.ArgumentParser(description="Secure CLI Tool")
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Enable debug mode"
    )
    
    try:
        args = parser.parse_args()
        
        # Validate and sanitize input
        debug_mode = validate_input(str(args.debug))
        
        # Set up logging based on the debug mode
        setup_logging(debug_mode)
        
        # Main application logic
        logging.info("Starting application")
        
        # Example of using debug mode
        if debug_mode:
            logging.debug("Debug mode is enabled")
            
        logging.info("Application finished")
        
    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()