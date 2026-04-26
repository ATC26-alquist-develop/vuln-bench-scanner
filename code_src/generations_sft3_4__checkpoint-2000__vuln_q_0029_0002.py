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
            raise FileNotFoundError(f"File not found: {filename}")
            
        # Use os.popen() with timeout to prevent hanging
        cmd = ['cat', abs_path]
        process = os.popen(' '.join(cmd), 'r')
        
        # Read and print file contents line by line
        while True:
            line = process.readline()
            if not line:
                break
            print(line.decode('utf-8').strip())
            
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <filename>", file=sys.stderr)
        sys.exit(1)
    
    display_file_contents(sys.argv[1])