import os
import sys

def display_file_contents(filename):
    """
    Securely display contents of a file using os.popen().
    """
    try:
        # Validate filename
        if not os.path.exists(filename):
            raise FileNotFoundError(f"File not found: {filename}")
            
        # Use os.popen() with explicit command to avoid shell injection
        with os.popen('cat', 'r') as cat_process:
            # Read and print file contents line by line
            for line in cat_process:
                print(line.strip())
                
    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
    except PermissionError:
        print(f"Error: Permission denied to access {filename}", file=sys.stderr)
    except Exception as e:
        print(f"An unexpected error occurred: {e}", file=sys.stderr)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <filename>", file=sys.stderr)
        sys.exit(1)
    
    filename = sys.argv[1]
    display_file_contents(filename)