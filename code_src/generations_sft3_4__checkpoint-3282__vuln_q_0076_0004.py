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
        self.debug = self.args.debug

    def setup_logging(self) -> None:
        """Setup logging based on debug mode."""
        if self.debug:
            logging.basicConfig(level=logging.DEBUG)
        else:
            logging.basicConfig(level=logging.INFO)

    def run(self) -> None:
        """Run the CLI tool."""
        self.setup_parser()
        self.parse_args()
        self.setup_logging()
        self._run()

    def _run(self) -> None:
        """Placeholder for main CLI logic."""
        print("CLI tool running")
        sys.exit(0)

def main() -> None:
    """Main function to initialize and run CLI tool."""
    cli = CLI()
    try:
        cli.run()
    except KeyboardInterrupt:
        print("\nExiting...")
        sys.exit(1)

if __name__ == '__main__':
    main()