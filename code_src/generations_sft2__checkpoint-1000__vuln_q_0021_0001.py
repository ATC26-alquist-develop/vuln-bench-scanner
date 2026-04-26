import xml.etree.ElementTree as ET
from typing import List, Dict
import re

class SecureXMLDatabase:
    def __init__(self, xml_file: str):
        """Initialize with XML file path, validate file exists and is readable."""
        if not isinstance(xml_file, str) or not xml_file:
            raise ValueError("Invalid XML file path")
        
        self.tree = ET.parse(xml_file)
        self.root = self.tree.getroot()

    def search_books_by_author(self, author_name: str) -> List[Dict[str, str]]:
        """Securely search books by author name."""
        if not isinstance(author_name, str) or not author_name.strip():
            raise ValueError("Invalid author name")
        
        # Sanitize input to prevent XML injection
        sanitized_author = re.sub(r'[^\w\s]', '', author_name)
        
        # Use XPath with parameterized query
        xpath_query = ".//book[author/text() = $author]"
        results = self.root.findall(xpath_query, {"author": sanitized_author})
        
        return [
            {
                "title": book.find("title").text,
                "author": book.find("author").text,
                "year": book.find("year").text
            }
            for book in results
        ]

# Usage example
if __name__ == "__main__":
    try:
        db = SecureXMLDatabase("books.xml")
        results = db.search_books_by_author("J.K. Rowling")
        for book in results:
            print(f"Title: {book['title']}, Author: {book['author']}, Year: {book['year']}")
    except Exception as e:
        print(f"Error: {str(e)}")