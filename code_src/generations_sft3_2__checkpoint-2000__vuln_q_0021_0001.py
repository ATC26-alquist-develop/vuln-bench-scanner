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
            # Use defusedxml for secure parsing
            tree = ET.parse(self.xml_file)
            root = tree.getroot()
            
            # Validate XML structure
            if root.tag != 'books':
                raise ValueError("Invalid XML structure")
            
            for book in root.findall('book'):
                if book.find('author') is not None and book.find('title') is not None:
                    self.books.append({
                        'author': self._sanitize_input(book.find('author').text),
                        'title': self._sanitize_input(book.find('title').text)
                    })
        except ET.ParseError:
            raise ValueError("Invalid XML file")
        except Exception as e:
            raise RuntimeError(f"Error loading books: {str(e)}")

    def _sanitize_input(self, input_str: str) -> str:
        """Sanitize input to prevent injection attacks."""
        if not input_str:
            return ''
        # Remove any non-alphanumeric characters except spaces
        return re.sub(r'[^\w\s]', '', input_str)

    def search_books(self, author: str) -> List[Dict[str, str]]:
        """Securely search for books by author."""
        if not author:
            return []
        # Sanitize input
        sanitized_author = self._sanitize_input(author)
        return [book for book in self.books if sanitized_author.lower() in book['author'].lower()]

    def get_book_info(self, book_id: int) -> Dict[str, str]:
        """Securely retrieve book information by ID."""
        if not isinstance(book_id, int) or book_id < 0:
            raise ValueError("Invalid book ID")
        if len(self.books) < book_id:
            raise IndexError("Book ID out of range")
        return self.books[book_id]

def main():
    try:
        db = SecureXMLDatabase('books.xml')
        while True:
            author = input("Enter author name (or 'q' to quit): ")
            if author.lower() == 'q':
                break
            
            results = db.search_books(author)
            if results:
                print("Matching books:")
                for book in results:
                    print(f"Title: {html.escape(book['title'])}")
            else:
                print("No matching books found.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()