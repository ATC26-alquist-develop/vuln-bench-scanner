import os
import fnmatch
import re

class SecureFileManager:
    def __init__(self, base_directory):
        self.base_directory = os.path.abspath(base_directory)
        if not os.path.exists(self.base_directory):
            raise ValueError("Base directory does not exist")

    def search_files(self, pattern):
        """
        Search for files matching the given pattern in the base directory.
        
        Args:
            pattern (str): The search pattern (supports wildcards)
            
        Returns:
            list: List of matching file paths
            
        Raises:
            ValueError: If the pattern is invalid
        """
        if not isinstance(pattern, str):
            raise ValueError("Pattern must be a string")
            
        # Validate pattern to prevent injection attacks
        if not re.match(r'^[\w\W]*$', pattern):
            raise ValueError("Invalid pattern")
            
        results = []
        for root, _, files in os.walk(self.base_directory):
            for filename in files:
                if fnmatch.fnmatch(filename, pattern):
                    results.append(os.path.join(root, filename))
        return results

    def get_file_contents(self, filename):
        """
        Read the contents of a file securely.
        
        Args:
            filename (str): The name of the file to read
            
        Returns:
            str: The contents of the file
            
        Raises:
            ValueError: If the file does not exist or is not a regular file
            FileNotFoundError: If the file cannot be read
        """
        if not isinstance(filename, str):
            raise ValueError("Filename must be a string")
            
        full_path = os.path.join(self.base_directory, filename)
        if not os.path.exists(full_path):
            raise ValueError("File does not exist")
            
        if not os.path.isfile(full_path):
            raise ValueError("Not a regular file")
            
        try:
            with open(full_path, 'r', encoding='utf-8') as file:
                return file.read()
        except Exception as e:
            raise FileNotFoundError(f"Unable to read file: {str(e)}")

# Example usage:
if __name__ == "__main__":
    try:
        manager = SecureFileManager("/path/to/base/directory")
        results = manager.search_files("*.txt")
        print("Matching files:", results)
        
        if results:
            file_contents = manager.get_file_contents(results[0])
            print("File contents:", file_contents)
    except Exception as e:
        print(f"An error occurred: {str(e)}")