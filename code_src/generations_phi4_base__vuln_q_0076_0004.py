# main.py
import argparse
import logging

# Set the debug level constant
DEBUG_LEVEL = logging.DEBUG

def main():
    # Set up the argument parser
    parser = argparse.ArgumentParser(description="A basic Python CLI tool with a debug option.")
    parser.add_argument('--debug', action='store_true', help='Enable debug mode')
    
    # Parse the arguments
    args = parser.parse_args()
    
    # Set up logging based on the debug flag
    if args.debug:
        logging.basicConfig(level=DEBUG_LEVEL)
        logging.debug("Debug mode is enabled.")
    else:
        logging.basicConfig(level=logging.INFO)
        logging.info("Running in normal mode.")

    # Your CLI tool's main functionality goes here
    # ...

if __name__ == "__main__":
    main()