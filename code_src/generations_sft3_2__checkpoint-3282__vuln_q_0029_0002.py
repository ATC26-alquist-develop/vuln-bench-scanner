import os
import sys

def display_file_contents(filename):
    try:
        # Check if file exists and is a regular file
        if not os.path.isfile(filename):
            print(f"Error: '{filename}' is not a valid file")
            return

        # Check file permissions
        if not os.access(filename, os.R_OK):
            print(f"Error: No read permission for '{filename}'")
            return

        # Open file in read-only mode
        with open(filename, 'r') as file:
            # Read and display file contents line by line
            for line in file:
                print(line.strip())
                
    except IOError as e:
        print(f"Error reading file: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <filename>")
    else:
        display_file_contents(sys.argv[1])