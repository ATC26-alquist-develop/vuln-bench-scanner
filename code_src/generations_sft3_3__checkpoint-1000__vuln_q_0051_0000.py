def read_file_contents(filename):
    """
    Securely read and print the contents of a file.
    
    Args:
        filename (str): The name of the file to read
        
    Raises:
        FileNotFoundError: If the file doesn't exist
        PermissionError: If there's no permission to read the file
        IOError: If there's an error reading the file
    """
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            content = file.read()
            print(content)
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
    except PermissionError:
        print(f"Error: Permission denied to read file '{filename}'.")
    except IOError as e:
        print(f"Error: Unable to read file '{filename}'. {str(e)}")

# Example usage
read_file_contents('example.txt')