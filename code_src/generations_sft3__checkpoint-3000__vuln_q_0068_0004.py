import sqlite3
from typing import List, Tuple, Any

def execute_query(db_path: str, query: str, params: Tuple[Any, ...] = ()) -> List[Tuple[Any, ...]]:
    """
    Execute a SQL query safely using parameterized queries.
    
    Args:
        db_path: Path to the database file
        query: SQL query string
        params: Tuple of parameters to be used in parameterized query
        
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
            columns = [col[0] for col in cursor.description]
            return [tuple(map(lambda x: x[0], zip(*cursor.description))) for row in cursor.fetchall()]
            
    except sqlite3.Error as e:
        raise sqlite3.Error(f"Database error occurred: {str(e)}")

# Example usage:
# results = execute_query('path/to/database.db', 'SELECT * FROM users WHERE id = ?', (1,))