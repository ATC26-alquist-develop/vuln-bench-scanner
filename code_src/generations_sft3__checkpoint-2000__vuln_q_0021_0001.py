from defusedxml import ElementTree as ET
import re
from typing import List, Dict
import html

class SecureXMLDatabase:
    def __init__(self, xml_file: str):
        """Initialize with a secure XML file path."""
        self.xml_file = xml_file
        self.books: List[Dict[str, str]] = []
        self._load_books()

    def _load_books(self) -> None:
        """Securely load books from XML file."""
        try:
            tree = ET.parse(self.xml_file)
            root = tree.getroot()
            
            for book in root.findall('book'):
                title = book.find('title')
                author = book.find('author')
                if title is not None and author is not None:
                    self.books.append({
                        'title': self._sanitize_input(title.text),
                        'author': self._sanitize_input(author.text)
                    })
        except ET.ParseError:
            raise ValueError("Invalid XML file format")
        except Exception as e:
            raise RuntimeError(f"Error loading XML: {str(e)}")

    def _sanitize_input(self, input_str: str) -> str:
        """Sanitize input to prevent injection attacks."""
        # Remove any HTML tags
        input_str = re.sub(r'<[^>]+>', '', input_str)
        # Escape special XML characters
        return html.escape(input_str)

    def search_books(self, author: str) -> List[Dict[str, str]]:
        """Securely search for books by author."""
        if not author:
            raise ValueError("Author name cannot be empty")
        
        # Sanitize input
        author = self._sanitize_input(author)
        
        # Perform case-insensitive search
        return [
            book for book in self.books
            if author.lower() in book['author'].lower()
        ]

def main():
    try:
        db = SecureXMLDatabase('books.xml')
        while True:
            author = input("Enter author name (or 'q' to quit): ")
            if author.lower() == 'q':
                break
            
            results = db.search_books(author)
            if results:
                print("Search results:")
                for book in results:
                    print(f"- {book['title']}")
            else:
                print("No books found for that author.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()