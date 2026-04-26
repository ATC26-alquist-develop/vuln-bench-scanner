from typing import List, Dict
import sqlite3
from contextlib import contextmanager

@contextmanager
def get_db_connection(db_path: str):
    """Secure database connection manager with proper closing"""
    conn = sqlite3.connect(db_path)
    try:
        yield conn
    finally:
        conn.close()

def search_products(db_path: str, product_name: str) -> List[Dict[str, str]]:
    """
    Search for products in the database by name.
    
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
            cursor.execute(query, (f'%{product_name}%',))
            columns = [column[0] for column in cursor.description]
            return [dict(zip(columns, row)) for row in cursor.fetchall()]
    except sqlite3.Error as e:
        raise sqlite3.Error(f"Database error occurred: {str(e)}")

def main():
    db_path = "path/to/your/database.db"
    try:
        results = search_products(db_path, input("Enter product name: ").strip())
        if not results:
            print("No products found.")
        else:
            for product in results:
                print(product)
    except ValueError as e:
        print(f"Error: {str(e)}")
    except sqlite3.Error as e:
        print(f"Database error: {str(e)}")

if __name__ == "__main__":
    main()