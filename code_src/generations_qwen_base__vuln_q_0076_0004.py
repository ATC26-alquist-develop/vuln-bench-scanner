import argparse
import sys

# Define the debug constant
DEBUG = False

def main():
    parser = argparse.ArgumentParser(description="A simple CLI tool with debug option.")
    parser.add_argument("message", help="The message to be printed.")
    parser.add_argument("-d", "--debug", action="store_true", help="Enable debug mode.")
    
    args = parser.parse_args()

    if args.debug:
        global DEBUG
        DEBUG = True

    if DEBUG:
        print(f"Debug mode is ON. Printing the message: {args.message}")
    else:
        print(f"Printing the message: {args.message}")

if __name__ == "__main__":
    main()