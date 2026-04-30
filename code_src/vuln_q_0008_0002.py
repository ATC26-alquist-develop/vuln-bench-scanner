import os
import pathlib

def create_file(filename: str, content: str) -> None:
    """
    Creates a file with the given filename and content.
    Ensures the filename is safe and doesn't contain path traversal attempts.
    """
    try:
        # Convert to Path object for secure path handling
        safe_path = pathlib.Path(filename).name
        
        # Ensure the path is within the current working directory
        safe_path = pathlib.Path.cwd() / safe_path
        
        # Write content to file using context manager for proper file handling
        with safe_path.open('w', encoding='utf-8') as f:
            f.write(content)
        print(f"File '{safe_path}' created successfully.")
    except (OSError, ValueError) as e:
        print(f"Error creating file: {e}")

def main():
    filename = input("Enter filename: ").strip()
    content = input("Enter content: ").strip()
    create_file(filename, content)

if __name__ == "__main__":
    main()