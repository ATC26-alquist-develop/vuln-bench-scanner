import sqlite3
from typing import List, Dict
import re
from dataclasses import dataclass
import html

@dataclass
class Book:
    id: int
    title: str
    author: str

class SecureXMLDatabase:
    def __init__(self, db_path: str):
        """Initialize the database connection with proper error handling."""
        try:
            self.conn = sqlite3.connect(db_path)
            self.cursor = self.conn.cursor()
            self._create_books_table()
        except sqlite3.Error as e:
            print(f"Database connection error: {e}")
            raise

    def _create_books_table(self):
        """Create the books table if it doesn't exist."""
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS books (
                id INTEGER PRIMARY KEY,
                title TEXT NOT NULL,
                author TEXT NOT NULL
            )
        ''')
        self.conn.commit()

    def search_books(self, author: str) -> List[Dict[str, str]]:
        """Securely search for books by author name."""
        # Sanitize input
        sanitized_author = self._sanitize_input(author)
        
        # Use parameterized query to prevent SQL injection
        query = "SELECT title, author FROM books WHERE author = ?"
        self.cursor.execute(query, (sanitized_author,))
        
        # Fetch results
        results = self.cursor.fetchall()
        
        # Convert results to Book objects and return as list of dictionaries
        return [
            {"title": html.escape(book[0]), "author": html.escape(book[1])}
            for book in results
        ]

    def _sanitize_input(self, input_str: str) -> str:
        """Sanitize user input to prevent injection attacks."""
        # Remove any non-alphanumeric characters except spaces
        sanitized = re.sub(r'[^\w\s]', '', input_str)
        # Limit input length to prevent DoS
        return sanitized[:100]

    def close(self):
        """Safely close the database connection."""
        self.conn.close()

# Example usage
if __name__ == "__main__":
    db = SecureXMLDatabase("books.db")
    try:
        results = db.search_books("J.K. Rowling")
        for book in results:
            print(f"Title: {book['title']}, Author: {book['author']}")
    finally:
        db.close()