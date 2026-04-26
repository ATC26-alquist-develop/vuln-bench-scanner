import subprocess
import sys

def display_file_contents(filename):
    try:
        # Use subprocess to run the cat command
        result = subprocess.run(['cat', filename], capture_output=True, text=True, check=True)
        # Print the output of the cat command
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
    except FileNotFoundError:
        print(f"Error: The file '{filename}' does not exist.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python display_file_contents.py <filename>")
    else:
        filename = sys.argv[1]
        display_file_contents(filename)