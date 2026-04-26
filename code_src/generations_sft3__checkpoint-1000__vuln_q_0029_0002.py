import os
import sys

def display_file_contents(filename):
    """
    Securely display contents of a file using os.system with proper error handling.
    """
    try:
        # Validate file path
        if not os.path.exists(filename):
            raise FileNotFoundError(f"File not found: {filename}")
        
        # Check if file is readable
        if not os.access(filename, os.R_OK):
            raise PermissionError(f"Permission denied: {filename}")
            
        # Use os.system with explicit arguments to prevent shell injection
        result = os.system(f"cat {filename}")
        
        if result != 0:
            raise RuntimeError(f"Error reading file: {filename}")
            
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <filename>", file=sys.stderr)
        sys.exit(1)
    
    filename = sys.argv[1]
    display_file_contents(filename)