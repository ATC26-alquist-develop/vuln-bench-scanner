from typing import List, Dict
import sqlite3
from contextlib import contextmanager

@contextmanager
def get_db_connection(db_path: str):
    """Secure context manager for database connections"""
    conn = None
    try:
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        yield conn
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        raise
    finally:
        if conn:
            conn.close()

def search_products(db_path: str, product_name: str) -> List[Dict[str, str]]:
    """
    Search for products in the database by name
    
    Args:
        db_path: Path to the SQLite database file
        product_name: Name of the product to search for
        
    Returns:
        List of dictionaries containing product information
        
    Raises:
        sqlite3.Error: If there's a database error
        ValueError: If product_name is empty
    """
    if not product_name:
        raise ValueError("Product name cannot be empty")
        
    query = "SELECT * FROM products WHERE name LIKE ?"
    
    try:
        with get_db_connection(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(query, (f"%{product_name}%",))
            results = cursor.fetchall()
            
            return [dict(row) for row in results]
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        raise

def main():
    db_path = "path/to/your/database.db"
    while True:
        try:
            product_name = input("Enter product name to search (or 'q' to quit): ")
            if product_name.lower() == 'q':
                break
            
            results = search_products(db_path, product_name)
            if results:
                print("Search results:")
                for product in results:
                    print(f"ID: {product['id']}, Name: {product['name']}, Price: {product['price']}")
            else:
                print("No products found.")
        except ValueError as e:
            print(f"Error: {e}")
        except sqlite3.Error as e:
            print(f"Database error: {e}")

if __name__ == "__main__":
    main()