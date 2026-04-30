import xml.etree.ElementTree as ET
from defusedxml.ElementTree import parse
import re
from typing import Optional

class SecureXMLDatabase:
    def __init__(self, file_path: str):
        """Initialize with path to XML database file."""
        self.file_path = file_path
        self.tree: Optional[ET.Element] = None

    def _validate_author_name(self, author_name: str) -> bool:
        """Validate author name to prevent injection attacks."""
        # Only allow letters, spaces, and hyphens
        return bool(re.match(r'^[A-Za-z\s-]+$', author_name))

    def _sanitize_input(self, input_string: str) -> str:
        """Sanitize input to prevent XSS and other attacks."""
        return input_string.replace('<', '&lt;').replace('>', '&gt;')

    def load_database(self) -> None:
        """Securely load XML database."""
        try:
            # Use defusedxml for secure parsing
            self.tree = parse(self.file_path)
        except (ET.ParseError, FileNotFoundError, OSError) as e:
            raise SecurityError(f"Error loading database: {str(e)}")

    def search_books(self, author_name: str) -> list[str]:
        """Search for books by author name."""
        if not self.tree:
            raise ValueError("Database not loaded. Call load_database() first.")

        if not self._validate_author_name(author_name):
            raise ValueError("Invalid author name")

        sanitized_name = self._sanitize_input(author_name)
        
        results = []
        for book in self.tree.findall('.//book'):
            if book.find('author').text and sanitized_name.lower() in book.find('author').text.lower():
                results.append(book.find('title').text)

        return results

class SecurityError(Exception):
    """Custom exception for security-related errors."""
    pass

# Example usage
if __name__ == "__main__":
    try:
        db = SecureXMLDatabase("books.xml")
        db.load_database()
        
        author = input("Enter author's name: ")
        books = db.search_books(author)
        
        print("Books by this author:")
        for book in books:
            print(f"- {book}")
    except (ValueError, SecurityError) as e:
        print(f"Error: {str(e)}")