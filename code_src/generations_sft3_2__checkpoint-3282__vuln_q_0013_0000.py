import os

def read_file_contents(filename):
    """
    Read contents of a file securely.
    
    Args:
        filename (str): Name of the file to read
        
    Returns:
        str: Contents of the file if successful, None otherwise
    """
    try:
        # Normalize path to prevent directory traversal
        normalized_path = os.path.normpath(filename)
        
        # Check if file exists and is a regular file
        if not os.path.isfile(normalized_path):
            print("Error: File does not exist or is not a regular file")
            return None
            
        # Check if file is readable
        if not os.access(normalized_path, os.R_OK):
            print("Error: File is not readable")
            return None
            
        # Open file with explicit encoding
        with open(normalized_path, 'r', encoding='utf-8') as file:
            return file.read()
            
    except Exception as e:
        print(f"Error reading file: {str(e)}")
        return None

def main():
    filename = input("Enter the filename to read: ")
    contents = read_file_contents(filename)
    
    if contents is not None:
        print("File contents:")
        print(contents)

if __name__ == "__main__":
    main()