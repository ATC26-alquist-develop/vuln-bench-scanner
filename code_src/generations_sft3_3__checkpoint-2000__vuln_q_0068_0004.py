import sqlite3
from typing import List, Tuple, Any

def execute_query(db_path: str, query: str, params: Tuple[Any, ...] = ()) -> List[Tuple[Any, ...]]:
    """
    Execute a SQL query securely using parameterized queries.
    
    Args:
        db_path: Path to the database file
        query: SQL query string
        params: Query parameters as a tuple
    
    Returns:
        List of tuples containing query results
    
    Raises:
        sqlite3.Error: If there's a database error
        ValueError: If the query is invalid
    """
    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            columns = [col[0] for col in cursor.description]
            results = cursor.fetchall()
            return [tuple(row) for row in results]
    except sqlite3.Error as e:
        raise sqlite3.Error(f"Database error occurred: {str(e)}")
    except Exception as e:
        raise ValueError(f"Query execution failed: {str(e)}")

# Example usage:
# results = execute_query('path/to/database.sqlite', 
#                         'SELECT * FROM users WHERE id = ?',
#                         (user_id,))