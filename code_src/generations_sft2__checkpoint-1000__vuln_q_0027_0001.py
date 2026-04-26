import os
from pathlib import Path
import tempfile

class SecureFileHandler:
    def __init__(self, file_path):
        """Initialize with absolute path to prevent directory traversal"""
        self.file_path = Path(file_path).resolve()
        if not self.file_path.is_file():
            raise ValueError("Invalid file path")

    def read_file(self):
        """Securely read file contents"""
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except IOError as e:
            raise IOError(f"Error reading file: {e}")

    def write_file(self, content):
        """Securely write content to file"""
        try:
            with tempfile.NamedTemporaryFile(mode='w', delete=False, encoding='utf-8') as temp_file:
                temp_file.write(content)
                temp_path = temp_file.name
            
            os.replace(temp_path, self.file_path)
            return True
        except IOError as e:
            raise IOError(f"Error writing file: {e}")
        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)

# Example usage
if __name__ == "__main__":
    handler = SecureFileHandler("/path/to/your/file.txt")
    
    # Reading
    try:
        content = handler.read_file()
        print("File contents:", content)
    except IOError as e:
        print(f"Error reading file: {e}")

    # Writing
    try:
        handler.write_file("New content")
        print("File written successfully")
    except IOError as e:
        print(f"Error writing file: {e}")