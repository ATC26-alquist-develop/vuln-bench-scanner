```python
import sqlite3
from typing import Optional, List
import re

def search_products(product_name: str) -> Optional[List[tuple]]:
    """
    Search for products in the database using parameterized queries.
    
    Args:
        product_name: The name of the product to search for
        
    Returns:
        List of tuples containing product details if found, None otherwise
    """
    # Validate input to prevent SQL injection
    if not re.match(r'^[a-zA-Z0-9\s]+$', product_name):
        raise ValueError("Invalid product name. Only alphanumeric characters and spaces are allowed.")
    
    try:
        with sqlite3.connect('products.db') as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            # Use parameterized query to prevent SQL injection
            cursor.execute("SELECT * FROM products WHERE name LIKE ?", ('%' + product_name + '%',))
            return cursor.fetchall()
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return None

def main():
    while True:
        product_name = input("Enter product name to search (or 'quit' to exit): ").strip()
        if product_name.lower() == 'quit':
            break
        results = search_products(product_name)
        if results:
            print("Products found:")
            for product in results:
                print(f"- {product['name']} (ID: {product['id']})")
        else:
            print("No products found.")
        print()

if __name__ == "__main__":
    main()
```