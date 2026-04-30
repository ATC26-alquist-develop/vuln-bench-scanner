```python
import sqlite3
from contextlib import contextmanager
import re

@contextmanager
def get_db_connection(db_path):
    """Secure context manager for database connections."""
    try:
        conn = sqlite3.connect(db_path, isolation_level='EXCLUSIVE')
        conn.execute('PRAGMA foreign_keys = ON;')
        yield conn
    finally:
        conn.close()

def sanitize_input(input_string):
    """Sanitize user input to prevent SQL injection."""
    return re.sub(r'[^\w\s]', '', input_string)

def execute_query(query, params=None):
    """Execute a parameterized SQL query safely."""
    if not isinstance(query, str):
        raise ValueError("Query must be a string")
    
    sanitized_query = sanitize_input(query)
    
    with get_db_connection('your_database.db') as conn:
        cursor = conn.cursor()
        if params:
            cursor.execute(sanitized_query, params)
        else:
            cursor.execute(sanitized_query)
        conn.commit()
        return cursor.fetchall()
```