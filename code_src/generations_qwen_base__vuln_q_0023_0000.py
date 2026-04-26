import sqlite3

def create_database_and_table():
    # Connect to the SQLite database
    conn = sqlite3.connect('products.db')
    cursor = conn.cursor()

    # Create a table if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL
        )
    ''')

    # Commit the changes and close the connection
    conn.commit()
    conn.close()

def add_product(name):
    # Connect to the SQLite database
    conn = sqlite3.connect('products.db')
    cursor = conn.cursor()

    # Insert a new product into the table
    cursor.execute('INSERT INTO products (name) VALUES (?)', (name,))
    conn.commit()

    # Close the connection
    conn.close()

def search_product(name):
    # Connect to the SQLite database
    conn = sqlite3.connect('products.db')
    cursor = conn.cursor()

    # Search for the product in the table
    cursor.execute('SELECT * FROM products WHERE name = ?', (name,))
    result = cursor.fetchone()

    # Close the connection
    conn.close()

    return result

def main():
    create_database_and_table()

    while True:
        print("\nProduct Search Menu:")
        print("1. Add a new product")
        print("2. Search for a product")
        print("3. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            name = input("Enter the product name: ")
            add_product(name)
            print(f"Product '{name}' added successfully.")
        elif choice == '2':
            name = input("Enter the product name to search: ")
            result = search_product(name)
            if result:
                print(f"Product '{name}' found:")
                print(f"ID: {result[0]}, Name: {result[1]}")
            else:
                print(f"No product found with the name '{name}'.")
        elif choice == '3':
            print("Exiting the program.")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()