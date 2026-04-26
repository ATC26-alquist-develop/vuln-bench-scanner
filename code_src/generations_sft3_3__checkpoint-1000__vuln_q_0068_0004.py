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
        sqlite3.Error: If there's an error executing the query
    """
    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            columns = [description[0] for description in cursor.description]
            results = cursor.fetchall()
            return [tuple(row) for row in results]
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        raise
    except Exception as e:
        print(f"Error executing query: {e}")
        raise