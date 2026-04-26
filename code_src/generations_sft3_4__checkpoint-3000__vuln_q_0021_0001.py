import sqlite3
from typing import List, Tuple
import re
from dataclasses import dataclass
from contextlib import contextmanager

@dataclass
class Book:
    id: int
    title: str
    author: str
    publication_year: int

class SecureXMLDatabase:
    def __init__(self, db_path: str):
        self.db_path = db_path
        self._create_tables()

    @contextmanager
    def _get_connection(self):
        """Secure connection management with proper closing"""
        conn = sqlite3.connect(self.db_path)
        try:
            yield conn
        finally:
            conn.close()

    def _create_tables(self):
        """Create tables with proper constraints"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS books (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    author TEXT NOT NULL,
                    publication_year INTEGER NOT NULL
                )
            ''')
            conn.commit()

    def _sanitize_input(self, input_str: str) -> str:
        """Sanitize user input to prevent SQL injection"""
        # Remove any non-alphanumeric characters except spaces
        return re.sub(r'[^\w\s]', '', input_str)

    def search_books_by_author(self, author_name: str) -> List[Book]:
        """Securely search for books by author name"""
        sanitized_author = self._sanitize_input(author_name)
        
        if not sanitized_author:
            raise ValueError("Author name cannot be empty after sanitization")

        with self._get_connection() as conn:
            cursor = conn.cursor()
            # Use parameterized query to prevent SQL injection
            query = "SELECT * FROM books WHERE author = ?"
            cursor.execute(query, (sanitized_author,))
            
            # Fetch results and convert to Book objects
            results = cursor.fetchall()
            return [Book(id=row[0], title=row[1], author=row[2], publication_year=row[3])
                    for row in results]

    def get_book_count(self) -> int:
        """Get total number of books in the database"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM books")
            return cursor.fetchone()[0]

# Example usage
if __name__ == "__main__":
    db = SecureXMLDatabase("books.db")
    try:
        results = db.search_books_by_author("J.K. Rowling")
        for book in results:
            print(f"ID: {book.id}, Title: {book.title}, Author: {book.author}, Year: {book.publication_year}")
    except ValueError as e:
        print(f"Error: {e}")