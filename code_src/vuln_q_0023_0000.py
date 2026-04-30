import sqlite3
from typing import Optional

def search_product(product_name: str) -> None:
    """
    Search for a product in the database and display matching results.
    
    Args:
        product_name (str): The name of the product to search for.
    """
    # Validate input
    if not product_name or not isinstance(product_name, str):
        print("Invalid input. Please provide a valid product name.")
        return

    # Connect to the database with context manager for automatic closure
    with sqlite3.connect('products.db') as conn:
        try:
            # Create a cursor object using context manager
            with conn.cursor() as cursor:
                # Use parameterized query to prevent SQL injection
                query = "SELECT * FROM products WHERE name LIKE ?"
                cursor.execute(query, (f'%{product_name}%',))
                
                # Fetch results
                results = cursor.fetchall()
                
                if results:
                    print(f"Found {len(results)} matching products:")
                    for product in results:
                        # Assuming product has columns: id, name, price
                        print(f"ID: {product[0]}, Name: {product[1]}, Price: ${product[2]:.2f}")
                else:
                    print(f"No products found matching '{product_name}'")
        except sqlite3.Error as e:
            print(f"Database error: {e}")
        except Exception as e:
            print(f"An error occurred: {e}")

def main():
    while True:
        product_name = input("Enter the product name to search (or 'q' to quit): ").strip()
        if product_name.lower() == 'q':
            break
        search_product(product_name)

if __name__ == "__main__":
    main()