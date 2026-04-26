import argparse
import sys
import logging
from typing import Optional

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CLI:
    def __init__(self):
        self.debug: bool = False

    def setup_parser(self) -> argparse.ArgumentParser:
        """Set up the argument parser with debug option."""
        parser = argparse.ArgumentParser(description='CLI Tool')
        parser.add_argument('--debug', action='store_true', help='Enable debug mode')
        return parser

    def parse_args(self, args: Optional[list] = None) -> None:
        """Parse command line arguments."""
        parser = self.setup_parser()
        self.args = parser.parse_args(args)

        if self.args.debug:
            logger.setLevel(logging.DEBUG)
            logger.debug("Debug mode enabled")

    def run(self, args: Optional[list] = None) -> None:
        """Run the CLI tool."""
        self.parse_args(args)
        logger.info("CLI tool started")

def main() -> None:
    """Main function to run the CLI tool."""
    cli = CLI()
    cli.run()

if __name__ == '__main__':
    main()