import sqlite3
from typing import List, Tuple, Any

def execute_query(db_path: str, query: str, params: Tuple[Any, ...] = ()) -> List[Tuple[Any, ...]]:
    """
    Execute a SQL query safely using parameterized queries.
    
    Args:
        db_path: Path to the database file
        query: SQL query string
        params: Query parameters to be safely inserted
        
    Returns:
        List of tuples containing query results
        
    Raises:
        sqlite3.Error: If there's a database error
        ValueError: If query is empty
    """
    if not query or not isinstance(query, str):
        raise ValueError("Query cannot be empty")
        
    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            return cursor.fetchall()
            
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        raise

# Example usage:
# results = execute_query('path/to/db.sqlite', 'SELECT * FROM users WHERE id = ?', (1,))