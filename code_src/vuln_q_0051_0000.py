```python
import os

def read_file_safely(file_path: str) -> None:
    """
    Safely read and print the contents of a file.
    
    Args:
        file_path: Path to the file to be read
        
    Raises:
        FileNotFoundError: If the file does not exist
        PermissionError: If the file cannot be accessed due to permission issues
        UnicodeDecodeError: If the file cannot be decoded using UTF-8
    """
    if not isinstance(file_path, str):
        raise TypeError("file_path must be a string")
        
    if not file_path:
        raise ValueError("file_path cannot be empty")
        
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            print(content)
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' does not exist.")
    except PermissionError:
        print(f"Error: Permission denied when accessing '{file_path}'.")
    except UnicodeDecodeError:
        print(f"Error: Unable to decode '{file_path}' using UTF-8 encoding.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

# Example usage:
# read_file_safely('example.txt')
```