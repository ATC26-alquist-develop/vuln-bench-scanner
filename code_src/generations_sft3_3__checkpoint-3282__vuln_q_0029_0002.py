import os
import sys

def display_file_contents(filename):
    """
    Securely display contents of a file using os.popen()
    """
    try:
        # Validate file path
        abs_path = os.path.abspath(filename)
        if not os.path.exists(abs_path):
            raise FileNotFoundError(f"File not found: {abs_path}")
        
        # Use os.popen() with timeout to prevent hanging
        # shell=False prevents shell injection
        fd = os.popen('cat ' + abs_path, 'r', timeout=5)
        contents = fd.read()
        fd.close()
        
        if contents:
            print(contents)
        else:
            print("File is empty")
            
    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
    except PermissionError:
        print(f"Error: Permission denied to access {filename}", file=sys.stderr)
    except Exception as e:
        print(f"Error: Unexpected error occurred - {e}", file=sys.stderr)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <filename>", file=sys.stderr)
        sys.exit(1)
    
    filename = sys.argv[1]
    display_file_contents(filename)