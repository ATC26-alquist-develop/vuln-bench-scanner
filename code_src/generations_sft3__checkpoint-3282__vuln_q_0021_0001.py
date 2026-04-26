from defusedxml import ElementTree as ET
import re
from typing import List, Dict
import html

class SecureXMLDatabase:
    def __init__(self, xml_file: str):
        """Initialize with a protected XML file path."""
        self.xml_file = xml_file
        self.books: List[Dict[str, str]] = []
        self._load_books()

    def _load_books(self) -> None:
        """Securely load books from XML file."""
        try:
            tree = ET.parse(self.xml_file)
            root = tree.getroot()
            
            for book in root.findall('book'):
                title = book.findtext('title')
                author = book.findtext('author')
                if title and author:
                    self.books.append({
                        'title': self._sanitize_input(title),
                        'author': self._sanitize_input(author)
                    })
        except ET.ParseError:
            raise ValueError("Invalid XML file format")
        except Exception as e:
            raise RuntimeError(f"Error loading books: {str(e)}")

    def _sanitize_input(self, input_str: str) -> str:
        """Sanitize user input to prevent injection attacks."""
        # Remove any non-alphanumeric characters except spaces
        return re.sub(r'[^\w\s]', '', html.escape(input_str))

    def search_books(self, author: str) -> List[Dict[str, str]]:
        """Securely search for books by author name."""
        sanitized_author = self._sanitize_input(author)
        return [book for book in self.books if sanitized_author.lower() in book['author'].lower()]

    def get_book_details(self, book_id: int) -> Dict[str, str]:
        """Securely retrieve book details by ID."""
        if not isinstance(book_id, int) or book_id < 0 or book_id >= len(self.books):
            raise ValueError("Invalid book ID")
        return self.books[book_id]

# Example usage
if __name__ == "__main__":
    db = SecureXMLDatabase("books.xml")
    try:
        results = db.search_books("J.K. Rowling")
        for book in results:
            print(f"Title: {book['title']}")
    except Exception as e:
        print(f"Error: {str(e)}")