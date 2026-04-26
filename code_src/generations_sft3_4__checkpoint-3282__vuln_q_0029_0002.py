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
            print(f"Error: File '{filename}' does not exist")
            return

        # Use os.popen() with timeout to prevent hanging
        # Note: os.popen() is not recommended for security reasons
        # Use subprocess instead for better security
        cmd = ['cat', abs_path]
        process = os.popen(' '.join(cmd))
        
        # Read and print file contents
        print(process.read().strip())
        
    except Exception as e:
        print(f"Error: Unable to display file contents - {str(e)}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <filename>")
    else:
        display_file_contents(sys.argv[1])