import os
import sys

def display_file_contents(filename):
    """
    Securely display contents of a file using os.popen()
    """
    try:
        # Validate file path
        if not os.path.exists(filename):
            raise FileNotFoundError(f"File not found: {filename}")
        
        # Check if file is readable
        if not os.access(filename, os.R_OK):
            raise PermissionError(f"No read permission for file: {filename}")
            
        # Use os.popen() with timeout to prevent hanging
        with os.popen('cat ' + filename, 'r', timeout=5) as f:
            print(f.read())
            
    except (FileNotFoundError, PermissionError) as e:
        print(f"Error: {e}", file=sys.stderr)
    except Exception as e:
        print(f"An unexpected error occurred: {e}", file=sys.stderr)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <filename>", file=sys.stderr)
        sys.exit(1)
    
    filename = sys.argv[1]
    display_file_contents(filename)