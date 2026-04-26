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
        self.logger.debug(f"CLI args: {self.args}")
        self.debug = self.args.debug

    def run(self, args: Optional[list] = None) -> None:
        self.parse_args(args)
        if self.debug:
            self.logger.setLevel(logging.DEBUG)
            self.logger.debug("Debug mode enabled")
        self._run()

    def _run(self) -> None:
        raise NotImplementedError("Subclasses must implement this method")

def main():
    cli = CLI()
    cli.run()

if __name__ == '__main__':
    main()