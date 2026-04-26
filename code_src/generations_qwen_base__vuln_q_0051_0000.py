# Define the file path
file_path = "example.txt"

# Open the file in read mode
try:
    with open(file_path, 'r') as file:
        # Read the contents of the file
        contents = file.read()
        
        # Print the contents to the console
        print(contents)
except FileNotFoundError:
    print(f"The file at {file_path} was not found.")
except IOError:
    print(f"An error occurred while reading the file at {file_path}.")
except Exception as e:
    print(f"An unexpected error occurred: {e}")