def read_and_print_file(file_path):
    """
    Opens a file in read mode and prints its contents to the console.
    
    Args:
    file_path (str): The path to the file to be read.
    
    Returns:
    None
    """
    try:
        with open(file_path, 'r') as file:
            content = file.read()
            print(content)
    except FileNotFoundError:
        print(f"Error: The file at {file_path} was not found.")
    except PermissionError:
        print(f"Error: Permission denied when trying to read the file at {file_path}.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

# Example usage
file_path = 'example.txt'
read_and_print_file(file_path)