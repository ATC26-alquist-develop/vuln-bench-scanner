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
        parser = argparse.ArgumentParser(description="CLI Tool")
        parser.add_argument('--debug', action='store_true', help='Enable debug mode')
        return parser

    def parse_args(self, args: Optional[list] = None) -> argparse.Namespace:
        parser = self.setup_parser()
        return parser.parse_args(args)

    def run(self, args: argparse.Namespace) -> None:
        if args.debug:
            logger.setLevel(logging.DEBUG)
            logger.debug("Debug mode enabled")
        else:
            logger.setLevel(logging.INFO)

        # Main logic here
        logger.info("CLI running")

def main() -> None:
    cli = CLI()
    args = cli.parse_args()
    cli.run(args)

if __name__ == "__main__":
    main()