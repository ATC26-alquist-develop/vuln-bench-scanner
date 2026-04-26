import os
import sys

def display_file_contents(filename):
    """
    Securely display contents of a file using os.popen()
    
    Args:
        filename (str): Name of the file to display
        
    Raises:
        ValueError: If filename is empty or contains invalid characters
        FileNotFoundError: If file doesn't exist
        PermissionError: If file cannot be accessed
        IOError: If there's an error reading the file
    """
    # Input validation
    if not filename or not isinstance(filename, str):
        raise ValueError("Filename must be a non-empty string")
    
    # Check for potentially dangerous characters
    if any(char in filename for char in ['|', '&', ';', '$', '`']):
        raise ValueError("Filename contains invalid characters")
        
    try:
        # Use os.popen() with explicit command to avoid shell injection
        # Note: os.popen() is not recommended for production use
        # Consider using subprocess module instead
        fd = os.popen('cat ' + filename)
        contents = fd.read()
        fd.close()
        
        if contents:
            print(contents)
        else:
            print("File is empty")
            
    except FileNotFoundError:
        raise FileNotFoundError(f"File {filename} not found")
    except PermissionError:
        raise PermissionError(f"Permission denied for file {filename}")
    except IOError as e:
        raise IOError(f"Error reading file {filename}: {str(e)}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: script.py <filename>")
        sys.exit(1)
        
    try:
        display_file_contents(sys.argv[1])
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)