import os
import subprocess
import sys

def display_file_contents(filename):
    """
    Display the contents of a file using the 'cat' command.
    
    Args:
    filename (str): The name of the file to display.
    
    Raises:
    ValueError: If the file does not exist or is not a regular file.
    """
    # Validate input
    if not isinstance(filename, str):
        raise ValueError("Filename must be a string")
    
    # Sanitize filename to prevent command injection
    filename = os.path.basename(filename)
    
    # Check if file exists and is a regular file
    if not os.path.exists(filename) or not os.path.isfile(filename):
        raise ValueError(f"File '{filename}' does not exist or is not a regular file")
    
    # Use a list to pass arguments to subprocess to prevent shell injection
    cmd = ['cat', filename]
    
    try:
        # Run the 'cat' command securely without using shell=True
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Error displaying file contents: {e}", file=sys.stderr)

# Example usage
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <filename>", file=sys.stderr)
        sys.exit(1)
    
    display_file_contents(sys.argv[1])