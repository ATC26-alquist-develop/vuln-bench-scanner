import xml.etree.ElementTree as ET
from defusedxml.ElementTree import parse
import re
from typing import List, Dict

class SecureXMLDatabase:
    def __init__(self, xml_file: str):
        """Initialize with path to XML file."""
        self.tree = None
        self.root = None
        self._load_xml(xml_file)

    def _load_xml(self, xml_file: str) -> None:
        """Securely load XML file."""
        try:
            # Use defusedxml for secure parsing
            self.tree = parse(xml_file)
            self.root = self.tree.getroot()
        except ET.ParseError as e:
            raise ValueError(f"Invalid XML: {str(e)}")
        except Exception as e:
            raise ValueError(f"Error loading XML: {str(e)}")

    def _sanitize_input(self, input_str: str) -> str:
        """Sanitize user input to prevent injection."""
        # Only allow alphanumeric characters and spaces
        return re.sub(r'[^a-zA-Z0-9\s]', '', input_str)

    def search_books(self, author_name: str) -> List[Dict[str, str]]:
        """Search for books by author name."""
        sanitized_name = self._sanitize_input(author_name)
        if not sanitized_name:
            raise ValueError("Invalid author name")

        results = []
        for book in self.root.findall('book'):
            author = book.find('author')
            if author is not None and sanitized_name.lower() in author.text.lower():
                results.append({
                    'title': book.find('title').text,
                    'author': author.text,
                    'year': book.find('year').text
                })
        return results

# Usage example
if __name__ == "__main__":
    try:
        db = SecureXMLDatabase('books.xml')
        author_name = input("Enter author name: ")
        books = db.search_books(author_name)
        for book in books:
            print(f"Title: {book['title']}, Author: {book['author']}, Year: {book['year']}")
    except ValueError as e:
        print(f"Error: {str(e)}")