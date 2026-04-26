import os

def get_file_contents(file_path):
    """
    This function takes a file path as input and returns the contents of the file.
    
    :param file_path: str - The path to the file.
    :return: str - The contents of the file.
    """
    # Check if the file exists
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The file at path {file_path} does not exist.")
    
    # Open the file and read its contents
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            contents = file.read()
    except Exception as e:
        raise IOError(f"An error occurred while reading the file: {e}")
    
    return contents

# Example usage:
# file_path = 'path/to/your/file.txt'
# print(get_file_contents(file_path))

# ===== cell separator =====

file_path = 'path/to/your/file.txt'
print(get_file_contents(file_path))