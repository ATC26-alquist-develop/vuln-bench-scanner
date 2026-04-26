import sqlite3
from typing import List, Tuple, Any

def execute_query(db_path: str, query: str, params: Tuple[Any, ...] = ()) -> List[Tuple[Any, ...]]:
    """
    Execute a SQL query safely using parameterized queries.
    
    Args:
        db_path: Path to the SQLite database file
        query: SQL query string
        params: Tuple of parameters to be used in parameterized query
        
    Returns:
        List of tuples containing query results
        
    Raises:
        sqlite3.Error: If there's a database error
        ValueError: If the query is empty
    """
    if not query.strip():
        raise ValueError("Query cannot be empty")
        
    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            columns = [col[0] for col in cursor.description]
            return [tuple(row) for row in cursor.fetchall()]
            
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        raise
    except Exception as e:
        print(f"Unexpected error: {e}")
        raise