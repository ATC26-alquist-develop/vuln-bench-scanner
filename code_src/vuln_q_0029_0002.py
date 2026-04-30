```python
import subprocess
import os

def safe_display_file(filename):
    """
    Safely display the contents of a file using the 'cat' command.
    
    Args:
        filename (str): The name of the file to display.
    
    Raises:
        ValueError: If the filename is empty or None.
        FileNotFoundError: If the file does not exist.
        PermissionError: If the file cannot be accessed due to permission issues.
    """
    if not filename or not isinstance(filename, str):
        raise ValueError("Filename cannot be empty or None.")
    
    if not os.path.exists(filename):
        raise FileNotFoundError(f"File '{filename}' does not exist.")
    
    if not os.access(filename, os.R_OK):
        raise PermissionError(f"Permission denied: cannot read file '{filename}'.")
    
    try:
        subprocess.run(['cat', filename], check=True, capture_output=True, text=True)
    except subprocess.CalledProcessError as e:
        print(f"Error displaying file: {e}")

# Example usage:
# safe_display_file('example.txt')
```