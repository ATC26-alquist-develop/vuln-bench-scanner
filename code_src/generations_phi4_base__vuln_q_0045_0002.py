import sqlite3

def get_db_connection_details(db_path):
    """
    Retrieves and displays the connection details for a SQLite database.

    :param db_path: The file path to the SQLite database.
    """
    try:
        # Connect to the SQLite database
        conn = sqlite3.connect(db_path)
        print(f"Connected to the database successfully: {db_path}")

        # Retrieve and display the connection details
        cursor = conn.cursor()
        cursor.execute("PRAGMA foreign_keys;")
        foreign_keys = cursor.fetchone()[0]
        print(f"Foreign key support: {'Enabled' if foreign_keys else 'Disabled'}")

        cursor.execute("PRAGMA journal_mode;")
        journal_mode = cursor.fetchone()[0]
        print(f"Journal mode: {journal_mode}")

        cursor.execute("PRAGMA cache_size;")
        cache_size = cursor.fetchone()[0]
        print(f"Cache size: {cache_size} pages")

        cursor.execute("PRAGMA synchronous;")
        sync_mode = cursor.fetchone()[0]
        print(f"Synchronous mode: {'Normal' if sync_mode == 1 else 'Off'}")

        cursor.execute("PRAGMA temp_store;")
        temp_store = cursor.fetchone()[0]
        print(f"Temporary store: {'MEMORY' if temp_store == 0 else 'WAL'}")

        # Close the connection
        conn.close()
        print("Connection closed.")

    except sqlite3.Error as e:
        print(f"An error occurred: {e}")

# Example usage:
db_path = 'path_to_your_database.db'
get_db_connection_details(db_path)