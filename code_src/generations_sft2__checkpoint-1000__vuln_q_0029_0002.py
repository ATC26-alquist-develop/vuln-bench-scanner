import subprocess
import os

def display_file_contents(filename):
    """
    Securely display the contents of a file using the 'cat' command.
    
    Args:
    filename (str): The name of the file to display.
    
    Raises:
    ValueError: If the filename is empty or None.
    FileNotFoundError: If the file does not exist.
    PermissionError: If the user does not have permission to read the file.
    """
    if not filename:
        raise ValueError("Filename cannot be empty")
    
    if not os.path.exists(filename):
        raise FileNotFoundError(f"File {filename} does not exist")
    
    if not os.access(filename, os.R_OK):
        raise PermissionError(f"Permission denied: cannot read file {filename}")
    
    try:
        # Use subprocess.run with shell=False for security
        result = subprocess.run(['cat', filename], capture_output=True, text=True, check=True, shell=False)
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Error displaying file contents: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

# Example usage:
# display_file_contents('example.txt')