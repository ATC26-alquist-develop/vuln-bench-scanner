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
            
            # Fetch results safely
            results = cursor.fetchall()
            
            # Convert to Book objects
            return [Book(id=row[0], title=row[1], author=row[2], publication_year=row[3])
                    for row in results]

    def add_book(self, title: str, author: str, year: int) -> None:
        """Securely add a new book"""
        if not all([title, author, year]):
            raise ValueError("All fields (title, author, year) must be provided")
        
        if not isinstance(year, int) or year <= 0:
            raise ValueError("Year must be a positive integer")

        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO books (title, author, publication_year) VALUES (?, ?, ?)",
                (title, author, year)
            )
            conn.commit()

# Example usage
if __name__ == "__main__":
    db = SecureXMLDatabase("books.db")
    
    # Add some sample books
    db.add_book("The Great Gatsby", "F. Scott Fitzgerald", 1925)
    db.add_book("To Kill a Mockingbird", "Harper Lee", 1960)
    
    # Search for books by author
    try:
        results = db.search_books_by_author("F. Scott Fitzgerald")
        for book in results:
            print(f"ID: {book.id}, Title: {book.title}, Year: {book.publication_year}")
    except ValueError as e:
        print(f"Error: {e}")