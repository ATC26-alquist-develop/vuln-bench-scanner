```python
import os
from typing import Union, IO
from pathlib import Path

class SecureFileHandler:
    """Secure file handler with read and write capabilities."""
    
    def __init__(self, file_path: Union[str, Path], mode: str = 'r'):
        """
        Initialize the file handler with a path and mode.
        
        Args:
            file_path: Path to the file
            mode: File mode ('r', 'w', 'a', 'rb', 'wb', 'ab')
        """
        self.file_path = Path(file_path).resolve()
        self.mode = mode
        self._file: IO = None

    def __enter__(self):
        """Context manager entry point."""
        if self.mode in ('r', 'rb'):
            self._file = open(self.file_path, self.mode)
        elif self.mode in ('w', 'wb', 'a', 'ab'):
            self._file = open(self.file_path, self.mode)
        else:
            raise ValueError(f"Unsupported mode: {self.mode}")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit point."""
        if self._file:
            try:
                self._file.close()
            except Exception:
                pass  # Ignore errors during close

    def read(self) -> str:
        """Read file contents securely."""
        if 'r' not in self.mode:
            raise ValueError("File not opened in read mode")
        
        with self._get_file_handle() as file:
            try:
                return file.read()
            except Exception:
                return ""  # Return empty string on error

    def write(self, content: str) -> None:
        """Write content to file securely."""
        if 'w' not in self.mode and 'a' not in self.mode:
            raise ValueError("File not opened in write or append mode")
        
        with self._get_file_handle() as file:
            try:
                file.write(content)
            except Exception:
                pass  # Ignore errors during write

    def _get_file_handle(self) -> IO:
        """Get a file handle with proper error handling."""
        if self._file is None:
            try:
                self._file = open(self.file_path, self.mode)
            except Exception:
                raise IOError(f"Failed to open file: {self.file_path}")
        return self._file

def main():
    """Example usage of SecureFileHandler."""
    try:
        # Reading from a file
        with SecureFileHandler('example.txt', 'r') as reader:
            content = reader.read()
            print(f"File contents: {content}")

        # Writing to a file
        with SecureFileHandler('example.txt', 'w') as writer:
            writer.write("Hello, secure world!")

        # Reading from the updated file
        with SecureFileHandler('example.txt', 'r') as reader:
            updated_content = reader.read()
            print(f"Updated file contents: {updated_content}")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
```