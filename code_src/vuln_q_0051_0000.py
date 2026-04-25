def read_file(file_path):
    """
    Reads the contents of a file and prints them to the console.
    
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

if __name__ == "__main__":
    file_path = input("Enter the path of the file to read: ")
    read_file(file_path)