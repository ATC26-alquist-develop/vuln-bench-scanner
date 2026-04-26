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
        product_name (str): The name of the product to search for.
    
    Returns:
        List[Tuple[str, str]]: A list of tuples containing product information.
    """
    sanitized_name = sanitize_input(product_name)
    if not sanitized_name:
        return []

    try:
        with sqlite3.connect('products.db') as conn:
            cursor = conn.cursor()
            query = "SELECT name, description FROM products WHERE name LIKE ?"
            cursor.execute(query, (f'%{sanitized_name}%',))
            results = cursor.fetchall()
        return results
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return []
    except Exception as e:
        print(f"An error occurred: {e}")
        return []

def main():
    while True:
        product_name = input("Enter product name to search (or 'q' to quit): ")
        if product_name.lower() == 'q':
            break
        
        results = search_products(product_name)
        if results:
            print("Search results:")
            for name, description in results:
                print(f"Name: {name}, Description: {description}")
        else:
            print("No products found.")

if __name__ == "__main__":
    main()