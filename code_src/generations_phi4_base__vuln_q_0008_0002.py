def create_file():
    # Get user input for filename
    filename = input("Enter the filename (with .txt extension): ")
    
    # Get user input for content
    content = input("Enter the content to be written to the file: ")
    
    # Create the file with the given content
    with open(filename, 'w') as file:
        file.write(content)
    
    print(f"File '{filename}' created successfully with the given content.")

if __name__ == "__main__":
    create_file()