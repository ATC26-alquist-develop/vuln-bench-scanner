import sqlite3
from typing import List, Tuple
import re

def sanitize_input(user_input: str) -> str:
    """Sanitize user input to prevent SQL injection."""
    return re.sub(r'[^\w\s]', '', user_input)

def search_products(product_name: str) -> List[Tuple[str, str]]:
    """
    Search for products in the database.
    
    Args:
        product_name: The name of the product to search for
        
    Returns:
        List of tuples containing product information (id, name)
    """
    # Sanitize input
    safe_name = sanitize_input(product_name)
    
    # Validate input
    if not safe_name:
        return []
    
    try:
        # Connect to database
        conn = sqlite3.connect('products.db')
        cursor = conn.cursor()
        
        # Use parameterized query to prevent SQL injection
        query = "SELECT id, name FROM products WHERE name LIKE ? LIMIT 100"
        cursor.execute(query, (f'%{safe_name}%',))
        
        results = cursor.fetchall()
        
        # Close connection
        conn.close()
        
        return results
    
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return []
    except Exception as e:
        print(f"Unexpected error: {e}")
        return []

def main():
    while True:
        user_input = input("Enter product name to search (or 'q' to quit): ")
        if user_input.lower() == 'q':
            break
        
        results = search_products(user_input)
        
        if results:
            print("Matching products:")
            for product_id, product_name in results:
                print(f"ID: {product_id}, Name: {product_name}")
        else:
            print("No matching products found.")

if __name__ == "__main__":
    main()