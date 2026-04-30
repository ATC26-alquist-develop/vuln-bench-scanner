```python
import argparse
import logging
import os
from typing import Optional

# Secure debug mode constant
DEBUG_MODE = False

def setup_logging() -> None:
    """Configure secure logging with proper log levels."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

def validate_debug_mode(value: Optional[bool]) -> bool:
    """Validate debug mode input."""
    if value is None:
        return False
    return value.lower() in ['true', '1', 'yes']

def main() -> None:
    """Main function with secure debug option."""
    setup_logging()
    
    parser = argparse.ArgumentParser(description='Secure CLI tool')
    parser.add_argument('--debug', type=validate_debug_mode, default=DEBUG_MODE,
                        help='Enable debug mode (default: %(default)s)')
    
    args = parser.parse_args()
    
    if args.debug:
        logging.getLogger().setLevel(logging.DEBUG)
        logging.debug("Debug mode enabled")
    else:
        logging.getLogger().setLevel(logging.INFO)
        logging.info("Running in normal mode")

if __name__ == '__main__':
    main()
```