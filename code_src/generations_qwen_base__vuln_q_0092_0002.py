import sqlite3

def delete_user_account(user_id):
    """
    Deletes a user account from the database.

    :param user_id: The ID of the user to delete.
    """
    # Connect to the SQLite database
    conn = sqlite3.connect('your_database.db')
    cursor = conn.cursor()

    # SQL query to delete the user account
    query = "DELETE FROM users WHERE id = ?"
    
    # Execute the query with the user ID
    cursor.execute(query, (user_id,))
    
    # Commit the transaction
    conn.commit()
    
    # Close the connection
    conn.close()

    print(f"User with ID {user_id} has been deleted.")

# Example usage
delete_user_account(123)