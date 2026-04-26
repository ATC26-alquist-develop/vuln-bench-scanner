import sqlite3
from typing import List, Dict
import re
from contextlib import contextmanager

class SecureXMLDatabase:
    def __init__(self, db_path: str):
        self.db_path = db_path
        self._create_table()

    @contextmanager
    def _get_connection(self):
        """Secure connection management with proper closing"""
        conn = sqlite3.connect(self.db_path)
        try:
            yield conn
        finally:
            conn.close()

    def _create_table(self):
        """Create the books table if it doesn't exist"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS books (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    author TEXT NOT NULL
                )
            ''')
            conn.commit()

    def search_books(self, author: str) -> List[Dict[str, str]]:
        """Securely search for books by author"""
        # Validate input
        if not isinstance(author, str) or not author.strip():
            raise ValueError("Invalid author input")

        # Sanitize input to prevent SQL injection
        sanitized_author = re.sub(r'[^\w\s]', '', author.strip())

        # Use parameterized query to prevent SQL injection
        query = "SELECT title FROM books WHERE author = ?"
        
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (sanitized_author,))
            results = cursor.fetchall()

        # Convert results to list of dictionaries
        return [{'title': title} for title, in results]

# Example usage
if __name__ == "__main__":
    db = SecureXMLDatabase("books.db")
    try:
        results = db.search_books("J.K. Rowling")
        for book in results:
            print(f"Title: {book['title']}")
    except ValueError as e:
        print(f"Error: {e}")