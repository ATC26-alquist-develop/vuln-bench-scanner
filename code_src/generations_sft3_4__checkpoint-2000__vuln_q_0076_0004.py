import argparse
import sys
import logging
from typing import Optional

class CLI:
    def __init__(self):
        self.debug: bool = False
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        ch = logging.StreamHandler(sys.stdout)
        ch.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        ch.setFormatter(formatter)
        self.logger.addHandler(ch)

    def setup_parser(self) -> argparse.ArgumentParser:
        parser = argparse.ArgumentParser(description='CLI Tool')
        parser.add_argument('--debug', action='store_true', help='Enable debug mode')
        return parser

    def parse_args(self, args: Optional[list] = None) -> None:
        parser = self.setup_parser()
        self.args = parser.parse_args(args)

    def run(self, args: Optional[list] = None) -> None:
        self.parse_args(args)
        self.logger.info(f"Debug mode: {self.debug}")
        self.logger.info(f"CLI arguments: {self.args}")

    def __call__(self, args: Optional[list] = None) -> None:
        self.run(args)

if __name__ == '__main__':
    cli = CLI()
    cli()