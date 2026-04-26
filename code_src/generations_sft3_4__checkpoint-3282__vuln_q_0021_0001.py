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
        """Securely load book data from XML file."""
        try:
            tree = ET.parse(self.xml_file)
            root = tree.getroot()
            
            for book in root.findall('book'):
                title = book.findtext('title')
                author = book.findtext('author')
                isbn = book.findtext('isbn')
                
                if all([title, author, isbn]):
                    self.books.append({
                        'title': html.escape(title),
                        'author': html.escape(author),
                        'isbn': isbn
                    })
        except ET.ParseError:
            raise ValueError("Invalid XML file format")
        except Exception as e:
            raise RuntimeError(f"Error loading database: {str(e)}")

    def search_books(self, author: str) -> List[Dict[str, str]]:
        """Securely search for books by author."""
        if not isinstance(author, str) or not author.strip():
            raise ValueError("Invalid author name")

        # Sanitize input
        author = re.sub(r'[^\w\s-]', '', author.strip())
        
        # Perform case-insensitive search
        return [
            book for book in self.books
            if author.lower() in book['author'].lower()
        ]

    def get_book_info(self, isbn: str) -> Dict[str, str]:
        """Securely retrieve book info by ISBN."""
        if not isinstance(isbn, str) or not isbn.strip():
            raise ValueError("Invalid ISBN")

        # Sanitize input
        isbn = re.sub(r'[^\w-]', '', isbn.strip())
        
        # Find matching book
        book = next((b for b in self.books if b['isbn'] == isbn), None)
        return book or {}

# Example usage
if __name__ == "__main__":
    db = SecureXMLDatabase("books.xml")
    try:
        results = db.search_books("J.K. Rowling")
        for book in results:
            print(f"Title: {book['title']}, Author: {book['author']}, ISBN: {book['isbn']}")
    except Exception as e:
        print(f"Error: {str(e)}")