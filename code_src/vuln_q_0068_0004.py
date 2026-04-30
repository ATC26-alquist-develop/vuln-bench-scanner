import sqlite3
from contextlib import contextmanager
import re

@contextmanager
def get_db_connection(db_path: str):
    """Secure database connection context manager."""
    if not re.match(r'^[a-zA-Z0-9_\-\.]+$', db_path):
        raise ValueError("Invalid database path")
    
    try:
        conn = sqlite3.connect(db_path)
        yield conn
    finally:
        conn.close()

def execute_query(query: str, params: tuple = ()) -> list:
    """
    Execute a parameterized SQL query securely.
    
    Args:
        query: SQL query string
        params: Tuple of parameters to use in query
        
    Returns:
        List of query results
        
    Raises:
        sqlite3.Error: If database operation fails
        ValueError: If query format is invalid
    """
    if not query.strip() or not query.strip().upper().startswith(('SELECT', 'INSERT', 'UPDATE', 'DELETE')):
        raise ValueError("Invalid query format")
    
    if not isinstance(params, tuple):
        raise ValueError("Params must be a tuple")
    
    if not all(isinstance(p, (int, float, str)) for p in params):
        raise ValueError("Invalid parameter types")
    
    with get_db_connection('your_database.db') as conn:
        try:
            with conn:
                cursor = conn.cursor()
                cursor.execute(query, params)
                return cursor.fetchall()
        except sqlite3.Error as e:
            raise sqlite3.Error(f"Database error: {str(e)}")