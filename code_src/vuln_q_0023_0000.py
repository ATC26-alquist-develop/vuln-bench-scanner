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
        
    # Validate input to prevent SQL injection
    if not product_name.replace(" ", "").isalnum():
        raise ValueError("Product name contains invalid characters")
        
    try:
        # Connect to the database
        with sqlite3.connect('products.db') as conn:
            # Create a cursor object
            cur = conn.cursor()
            
            # Use parameterized query to prevent SQL injection
            query = "SELECT * FROM products WHERE name LIKE ?"
            cur.execute(query, ('%' + product_name + '%',))
            
            # Fetch all matching rows
            results = cur.fetchall()
            
            return results
            
    except sqlite3.Error as e:
        # Log the error (in production, use proper logging)
        print(f"Database error: {e}")
        return None
    except Exception as e:
        # Log the error (in production, use proper logging)
        print(f"Unexpected error: {e}")
        return None

def main():
    try:
        product_name = input("Enter product name to search: ").strip()
        results = search_products(product_name)
        
        if results:
            print("Matching products:")
            for row in results:
                print(row)
        else:
            print("No products found")
            
    except ValueError as e:
        print(f"Invalid input: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()