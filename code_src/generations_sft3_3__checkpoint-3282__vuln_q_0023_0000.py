from typing import List
import sqlite3
from contextlib import contextmanager

@contextmanager
def get_db_connection(db_path: str):
    """Secure context manager for database connections"""
    conn = None
    try:
        conn = sqlite3.connect(db_path)
        yield conn
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        raise
    finally:
        if conn:
            conn.close()

def search_products(db_path: str, product_name: str) -> List[str]:
    """
    Search for products in the database by name
    
    Args:
        db_path: Path to the SQLite database file
        product_name: Name of the product to search for
        
    Returns:
        List of matching product names
        
    Raises:
        sqlite3.Error: If there's a database error
        ValueError: If product_name is empty
    """
    if not product_name:
        raise ValueError("Product name cannot be empty")
        
    try:
        with get_db_connection(db_path) as conn:
            cursor = conn.cursor()
            
            # Use parameterized query to prevent SQL injection
            query = "SELECT name FROM products WHERE name LIKE ?"
            cursor.execute(query, (f'%{product_name}%',))
            
            results = cursor.fetchall()
            return [row[0] for row in results]
            
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        raise

def main():
    db_path = "path/to/your/database.db"  # Replace with actual path
    try:
        results = search_products(db_path, input("Enter product name: ").strip())
        print("Matching products:")
        for product in results:
            print(product)
    except ValueError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()