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
    subprocess.SubprocessError: If an error occurs while executing the 'cat' command.
    """
    if not filename:
        raise ValueError("Filename cannot be empty")
    
    if not os.path.exists(filename):
        raise FileNotFoundError(f"File '{filename}' not found")
    
    if not os.access(filename, os.R_OK):
        raise PermissionError(f"Permission denied: cannot read file '{filename}'")
    
    try:
        # Use subprocess.run with shell=False for security
        result = subprocess.run(['cat', filename], 
                               capture_output=True, 
                               text=True, 
                               check=True, 
                               shell=False)
        print(result.stdout)
    except subprocess.SubprocessError as e:
        raise subprocess.SubprocessError(f"Error executing 'cat' command: {e}")

# Example usage:
# display_file_contents('example.txt')