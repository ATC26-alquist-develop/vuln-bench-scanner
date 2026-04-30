import defusedxml.ElementTree as ET
from defusedxml.ElementTree import ParseError
import re
from typing import List, Dict, Optional

class SecureBookDatabase:
    def __init__(self, xml_file: str):
        """Initialize with a path to a secure XML file."""
        self._xml_file = xml_file
        self._books: List[Dict[str, str]] = []
        self._load_books()

    def _load_books(self) -> None:
        """Securely load books from XML file."""
        try:
            tree = ET.parse(self._xml_file)
            root = tree.getroot()
            for book in root.findall('book'):
                self._books.append({
                    'title': book.find('title').text,
                    'author': book.find('author').text,
                    'year': book.find('year').text
                })
        except ParseError:
            raise ValueError("Invalid XML file")

    def search_books(self, author_name: str) -> List[Dict[str, str]]:
        """Securely search books by author name."""
        sanitized_name = self._sanitize_input(author_name)
        return [
            book for book in self._books
            if book['author'].lower() == sanitized_name.lower()
        ]

    @staticmethod
    def _sanitize_input(input_str: str) -> str:
        """Sanitize input to prevent injection attacks."""
        return re.sub(r'[^\w\s]', '', input_str).strip()

# Usage example
if __name__ == "__main__":
    db = SecureBookDatabase("books.xml")
    author = input("Enter author name: ")
    results = db.search_books(author)
    for book in results:
        print(f"Title: {book['title']}, Author: {book['author']}, Year: {book['year']}")