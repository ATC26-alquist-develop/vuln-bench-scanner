import sqlite3
from typing import List, Tuple, Any

def execute_query(db_path: str, query: str, params: Tuple[Any, ...] = ()) -> List[Tuple[Any, ...]]:
    """
    Execute a parameterized SQL query securely.
    
    Args:
        db_path: Path to the database file
        query: SQL query string
        params: Tuple of parameters to be used in the query
        
    Returns:
        List of tuples containing query results
        
    Raises:
        sqlite3.Error: If there's a database error
        ValueError: If the query is invalid
    """
    try:
        # Use context manager for automatic connection closing
        with sqlite3.connect(db_path) as conn:
            # Enable parameterized queries
            conn.set_trace_callback(print)
            
            # Create a cursor object
            cursor = conn.cursor()
            
            # Execute the query with parameters
            cursor.execute(query, params)
            
            # Fetch results
            columns = [column[0] for column in cursor.description]
            return [tuple(row) for row in cursor.fetchall()]
            
    except sqlite3.Error as e:
        # Log the error securely (implement proper logging)
        print(f"Database error: {e}")
        raise
    except Exception as e:
        # Log the error securely (implement proper logging)
        print(f"Error executing query: {e}")
        raise