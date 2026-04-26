import argparse
import sys
import logging
from typing import Optional

class CLI:
    def __init__(self):
        self.debug: bool = False
        self.parser = None
        self.args = None

    def setup_parser(self) -> None:
        """Setup the argument parser with debug option."""
        self.parser = argparse.ArgumentParser(description='CLI Tool')
        self.parser.add_argument('--debug', action='store_true', help='Enable debug mode')

    def parse_args(self) -> None:
        """Parse command line arguments."""
        self.args = self.parser.parse_args()

    def set_debug(self) -> None:
        """Set debug mode based on command line argument."""
        if self.args.debug:
            self.debug = True
        else:
            self.debug = False

    def run(self) -> None:
        """Run the CLI tool."""
        self.setup_parser()
        self.parse_args()
        self.set_debug()
        
        if self.debug:
            logging.basicConfig(level=logging.DEBUG)
            logging.debug("Debug mode enabled")

        # Main CLI logic would go here
        print("CLI running")

def main() -> None:
    cli = CLI()
    cli.run()

if __name__ == '__main__':
    main()