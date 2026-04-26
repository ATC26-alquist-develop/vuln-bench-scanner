def read_file_contents(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            contents = file.read()
            return contents
    except FileNotFoundError:
        return "Error: The file does not exist."
    except IOError:
        return "Error: An I/O error occurred while reading the file."
    except Exception as e:
        return f"An unexpected error occurred: {str(e)}"

def main():
    # Prompt the user for the filename
    filename = input("Enter the filename: ")
    
    # Read and print the contents of the file
    contents = read_file_contents(filename)
    print(f"Contents of {filename}:\n{contents}")

if __name__ == "__main__":
    main()