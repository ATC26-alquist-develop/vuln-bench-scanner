import os

def read_file_contents(file_path):
    # Check if the file exists
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"The file at {file_path} does not exist.")
    
    # Read and return the contents of the file
    with open(file_path, 'r') as file:
        contents = file.read()
    
    return contents

# Example usage:
# file_contents = read_file_contents('/path/to/your/file.txt')
# print(file_contents)