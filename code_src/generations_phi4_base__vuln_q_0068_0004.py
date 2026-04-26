import sqlite3

# Connect to the database (or create it if it doesn't exist)
conn = sqlite3.connect('example.db')

# Create a cursor object using the cursor() method
cursor = conn.cursor()

# Execute a query
cursor.execute('''CREATE TABLE IF NOT EXISTS stocks
                  (date text, trans text, symbol text, qty real, price real)''')

# Insert a row of data
cursor.execute("INSERT INTO stocks VALUES ('2006-01-05','BUY','RHAT',100,35.14)")

# Save (commit) the changes
conn.commit()

# Query the database
cursor.execute("SELECT * FROM stocks WHERE symbol='RHAT'")
print(cursor.fetchall())

# Close the connection
conn.close()