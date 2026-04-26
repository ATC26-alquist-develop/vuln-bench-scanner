import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('mydatabase.db')
cursor = conn.cursor()

# Execute a SQL query
cursor.execute("SELECT * FROM users")

# Fetch all rows from the executed query
rows = cursor.fetchall()

# Print the rows
for row in rows:
    print(row)

# Close the connection
conn.close()

# ===== cell separator =====

import psycopg2

# Database connection parameters
params = {
    'dbname': 'your_database',
    'user': 'your_username',
    'password': 'your_password',
    'host': 'your_host',
    'port': 'your_port'
}

# Connect to the PostgreSQL database
conn = psycopg2.connect(**params)
cursor = conn.cursor()

# Execute a SQL query
cursor.execute("SELECT * FROM users")

# Fetch all rows from the executed query
rows = cursor.fetchall()

# Print the rows
for row in rows:
    print(row)

# Close the connection
conn.close()

# ===== cell separator =====

import mysql.connector

# Database connection parameters
params = {
    'user': 'your_username',
    'password': 'your_password',
    'host': 'your_host',
    'database': 'your_database',
    'raise_on_warnings': True
}

# Connect to the MySQL database
conn = mysql.connector.connect(**params)
cursor = conn.cursor()

# Execute a SQL query
cursor.execute("SELECT * FROM users")

# Fetch all rows from the executed query
rows = cursor.fetchall()

# Print the rows
for row in rows:
    print(row)

# Close the connection
conn.close()