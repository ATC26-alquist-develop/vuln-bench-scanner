def create_file_with_content(filename, content):
    """
    Creates a file with the given filename and content.

    :param filename: The name of the file to create.
    :param content: The content to write into the file.
    """
    try:
        # Open the file in write mode
        with open(filename, 'w') as file:
            # Write the content to the file
            file.write(content)
        print(f"File '{filename}' created successfully with the given content.")
    except Exception as e:
        print(f"An error occurred: {e}")

def main():
    # Get user input for filename and content
    filename = input("Enter the filename: ")
    content = input("Enter the content to write into the file: ")

    # Create the file with the given content
    create_file_with_content(filename, content)

if __name__ == "__main__":
    main()