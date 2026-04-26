import argparse
import sys
import logging
from typing import Optional

class CLI:
    def __init__(self):
        self.debug: bool = False
        self.parser = argparse.ArgumentParser(description='CLI Tool')
        
    def setup_logging(self):
        """Configure logging based on debug mode"""
        if self.debug:
            logging.basicConfig(level=logging.DEBUG)
        else:
            logging.basicConfig(level=logging.INFO)

    def setup_parser(self):
        """Setup argument parser"""
        self.parser.add_argument('--debug', action='store_true', 
                                help='Enable debug mode')
        
    def parse_args(self):
        """Parse command line arguments"""
        self.setup_parser()
        args = self.parser.parse_args()
        self.debug = args.debug
        self.setup_logging()

    def run(self):
        """Main CLI execution"""
        self.parse_args()
        print(f"Debug mode: {'Enabled' if self.debug else 'Disabled'}")
        # Main CLI logic would go here
        sys.exit(0)

if __name__ == '__main__':
    CLI().run()