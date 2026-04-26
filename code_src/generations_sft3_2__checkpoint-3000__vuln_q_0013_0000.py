import os

def read_file_contents(filename):
    """
    Reads the contents of a file securely.
    
    Args:
        filename (str): The name of the file to read
        
    Returns:
        str: The contents of the file if successful, None otherwise
    """
    try:
        # Normalize the path to prevent directory traversal attacks
        normalized_path = os.path.normpath(filename)
        
        # Check if the file exists and is a regular file
        if not os.path.isfile(normalized_path):
            print("Error: File does not exist or is not a regular file")
            return None
            
        # Check if we have read permissions
        if not os.access(normalized_path, os.R_OK):
            print("Error: No read permission for the file")
            return None
            
        # Open file with explicit encoding to avoid encoding issues
        with open(normalized_path, 'r', encoding='utf-8') as file:
            contents = file.read()
            
        return contents
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None

def main():
    filename = input("Enter the filename to read: ")
    contents = read_file_contents(filename)
    
    if contents is not None:
        print("File contents:")
        print(contents)

if __name__ == "__main__":
    main()