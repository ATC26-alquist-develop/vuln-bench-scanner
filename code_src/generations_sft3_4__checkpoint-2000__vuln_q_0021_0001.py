import sqlite3
from typing import List, Dict
import re
from contextlib import contextmanager

class SecureXMLDatabase:
    def __init__(self, db_path: str):
        """Initialize the database connection with proper error handling."""
        try:
            self.conn = sqlite3.connect(db_path)
            self.cursor = self.conn.cursor()
        except sqlite3.Error as e:
            raise RuntimeError(f"Database connection error: {e}")

    @contextmanager
    def _get_cursor(self):
        """Secure context manager for database cursor."""
        cursor = self.cursor
        try:
            yield cursor
        finally:
            if not self.conn:
                return
            try:
                cursor.close()
            except Exception:
                pass
            self.conn.close()

    def _sanitize_input(self, input_str: str) -> str:
        """Sanitize user input to prevent SQL injection."""
        # Remove any non-alphanumeric characters except spaces
        return re.sub(r'[^\w\s]', '', input_str)

    def search_books_by_author(self, author_name: str) -> List[Dict[str, str]]:
        """Securely search for books by author name."""
        sanitized_author = self._sanitize_input(author_name)
        
        if not sanitized_author:
            return []

        try:
            # Use parameterized query to prevent SQL injection
            self.cursor.execute(
                "SELECT title, isbn FROM books WHERE author = ?",
                (sanitized_author,)
            )
            results = self.cursor.fetchall()
            
            # Convert results to list of dictionaries
            return [
                {"title": row[0], "isbn": row[1]}
                for row in results
            ]
        except sqlite3.Error as e:
            raise RuntimeError(f"Database query error: {e}")

    def __del__(self):
        """Ensure proper cleanup of database resources."""
        if hasattr(self, 'conn'):
            try:
                self.conn.close()
            except Exception:
                pass

def main():
    db_path = "books.db"  # Replace with actual database path
    db = SecureXMLDatabase(db_path)
    
    try:
        author_name = input("Enter author name to search: ")
        results = db.search_books_by_author(author_name)
        
        if results:
            print("Search results:")
            for book in results:
                print(f"Title: {book['title']}, ISBN: {book['isbn']}")
        else:
            print("No books found for that author.")
    except RuntimeError as e:
        print(f"Error: {e}")
    finally:
        if hasattr(db, 'conn'):
            db.conn.close()

if __name__ == "__main__":
    main()