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
        product_name (str): The name of the product to search for.
    
    Returns:
        List[Tuple[int, str, float]]: A list of tuples containing product ID, name, and price.
    """
    # Sanitize input
    safe_product_name = sanitize_input(product_name)
    
    # Validate input
    if not safe_product_name:
        return []
    
    try:
        # Connect to the database
        conn = sqlite3.connect('products.db')
        cursor = conn.cursor()
        
        # Use parameterized query to prevent SQL injection
        query = "SELECT id, name, price FROM products WHERE name LIKE ? LIMIT 100"
        cursor.execute(query, (f'%{safe_product_name}%',))
        
        # Fetch results
        results = cursor.fetchall()
        
        # Close database connection
        conn.close()
        
        return results
    
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return []
    except Exception as e:
        print(f"An error occurred: {e}")
        return []

def main():
    while True:
        user_input = input("Enter product name to search (or 'q' to quit): ")
        if user_input.lower() == 'q':
            break
        
        results = search_products(user_input)
        
        if results:
            print("Search results:")
            for product in results:
                print(f"ID: {product[0]}, Name: {product[1]}, Price: ${product[2]:.2f}")
        else:
            print("No products found.")

if __name__ == "__main__":
    main()