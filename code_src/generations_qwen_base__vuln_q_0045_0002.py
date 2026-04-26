import psycopg2

def display_database_connection_details():
    try:
        # Establish a connection to the PostgreSQL database
        connection = psycopg2.connect(
            dbname="your_database_name",
            user="your_username",
            password="your_password",
            host="your_host",
            port="your_port"
        )
        
        # Get the cursor object
        cursor = connection.cursor()
        
        # Retrieve the connection details
        cursor.execute("SHOW server_version;")
        server_version = cursor.fetchone()[0]
        
        cursor.execute("SHOW client_encoding;")
        client_encoding = cursor.fetchone()[0]
        
        cursor.execute("SHOW default_transaction_isolation;")
        default_transaction_isolation = cursor.fetchone()[0]
        
        cursor.execute("SHOW default_transaction_read_only;")
        default_transaction_read_only = cursor.fetchone()[0]
        
        cursor.execute("SHOW default_transaction_deferrable;")
        default_transaction_deferrable = cursor.fetchone()[0]
        
        cursor.execute("SHOW default_transaction_isolation;")
        default_transaction_isolation = cursor.fetchone()[0]
        
        cursor.execute("SHOW default_transaction_read_only;")
        default_transaction_read_only = cursor.fetchone()[0]
        
        cursor.execute("SHOW default_transaction_deferrable;")
        default_transaction_deferrable = cursor.fetchone()[0]
        
        # Display the connection details
        print(f"Server Version: {server_version}")
        print(f"Client Encoding: {client_encoding}")
        print(f"Default Transaction Isolation: {default_transaction_isolation}")
        print(f"Default Transaction Read Only: {default_transaction_read_only}")
        print(f"Default Transaction Deferrable: {default_transaction_deferrable}")
        
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Close the cursor and connection
        if cursor:
            cursor.close()
        if connection:
            connection.close()

# Call the function to display the connection details
display_database_connection_details()