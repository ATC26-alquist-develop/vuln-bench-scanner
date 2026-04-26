import sqlite3
from typing import Optional

def search_products(product_name: str) -> Optional[list]:
    """
    Search for products in the database by name.
    
    Args:
        product_name: The name of the product to search for
        
    Returns:
        A list of matching products or None if no products are found
    """
    if not isinstance(product_name, str):
        raise ValueError("Product name must be a string")
        
    if not product_name.strip():
        raise ValueError("Product name cannot be empty")
        
    try:
        # Connect to the database
        conn = sqlite3.connect('products.db')
        cursor = conn.cursor()
        
        # Use parameterized query to prevent SQL injection
        query = "SELECT * FROM products WHERE name LIKE ?"
        cursor.execute(query, (f"%{product_name}%",))
        
        # Fetch results
        results = cursor.fetchall()
        
        # Close connection
        conn.close()
        
        return results
        
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return None
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None

def main():
    while True:
        product_name = input("Enter product name to search (or 'quit' to exit): ").strip()
        
        if product_name.lower() == 'quit':
            break
            
        results = search_products(product_name)
        
        if results:
            print("Matching products:")
            for row in results:
                print(row)
        else:
            print("No products found")

if __name__ == "__main__":
    main()