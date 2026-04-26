import sqlite3
from typing import List, Tuple
import re

def sanitize_input(user_input: str) -> str:
    """Sanitize user input to prevent SQL injection."""
    return re.sub(r'[^\w\s]', '', user_input)

def search_products(product_name: str) -> List[Tuple[int, str, float]]:
    """
    Search for products in the database.
    
    Args:
        product_name: The name of the product to search for
        
    Returns:
        List of tuples containing (product_id, name, price)
    """
    # Sanitize input
    safe_name = sanitize_input(product_name)
    
    # Connect to database
    conn = sqlite3.connect('products.db')
    cursor = conn.cursor()
    
    try:
        # Use parameterized query to prevent SQL injection
        query = "SELECT * FROM products WHERE name LIKE ?"
        cursor.execute(query, (f'%{safe_name}%',))
        
        # Fetch results
        results = cursor.fetchall()
        return results
    
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return []
    
    finally:
        cursor.close()
        conn.close()

def main():
    while True:
        user_input = input("Enter product name to search (or 'q' to quit): ")
        if user_input.lower() == 'q':
            break
        
        results = search_products(user_input)
        
        if results:
            print("Search results:")
            for product_id, name, price in results:
                print(f"ID: {product_id}, Name: {name}, Price: ${price:.2f}")
        else:
            print("No products found.")

if __name__ == "__main__":
    main()