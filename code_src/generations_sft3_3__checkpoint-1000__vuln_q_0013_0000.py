import os

def read_file_contents(filename):
    """
    Securely read the contents of a file.
    
    Args:
        filename (str): The name of the file to read
        
    Returns:
        str: The contents of the file
        
    Raises:
        ValueError: If the file doesn't exist or is not a regular file
        IOError: If there's an error reading the file
    """
    # Validate filename
    if not isinstance(filename, str):
        raise ValueError("Filename must be a string")
    
    # Convert to absolute path and resolve any symlinks
    abs_path = os.path.abspath(os.path.realpath(filename))
    
    # Check if file exists and is a regular file
    if not os.path.isfile(abs_path):
        raise ValueError("File does not exist or is not a regular file")
    
    try:
        with open(abs_path, 'r', encoding='utf-8') as file:
            return file.read()
    except IOError as e:
        raise IOError(f"Error reading file: {e}")

def main():
    try:
        filename = input("Enter the filename to read: ")
        contents = read_file_contents(filename)
        print("File contents:")
        print(contents)
    except (ValueError, IOError) as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()