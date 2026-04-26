import sqlite3
from typing import Optional, List, Dict, Any
import re

class SecureDatabase:
    def __init__(self, db_path: str):
        """Initialize database connection with proper error handling."""
        try:
            self.connection = sqlite3.connect(db_path)
            self.cursor = self.connection.cursor()
        except sqlite3.Error as e:
            raise RuntimeError(f"Database connection failed: {e}")

    def _validate_query(self, query: str) -> bool:
        """Validate query to prevent SQL injection."""
        # Only allow alphanumeric characters, spaces, and basic SQL operators
        return bool(re.match(r'^[a-zA-Z0-9\s\(\)\[\]\{\}\.\,\s]+$', query))

    def execute_query(self, query: str, params: Optional[Dict[str, Any]] = None) -> Optional[List[Dict[str, Any]]]:
        """
        Execute a parameterized SQL query securely.
        
        Args:
            query: SQL query string
            params: Optional dictionary of parameters to use in query
            
        Returns:
            List of dictionaries containing query results
            
        Raises:
            ValueError: If query validation fails
            sqlite3.Error: If database operation fails
        """
        if not self._validate_query(query):
            raise ValueError("Invalid query format")

        try:
            if params:
                # Use parameterized query to prevent SQL injection
                self.cursor.execute(query, tuple(params.values()))
            else:
                self.cursor.execute(query)
            
            # Fetch results and convert to list of dictionaries
            columns = [description[0] for description in self.cursor.description]
            return [dict(zip(columns, row)) for row in self.cursor.fetchall()]
            
        except sqlite3.Error as e:
            raise sqlite3.Error(f"Database error: {e}")
        finally:
            # Ensure connection is closed
            self.connection.close()

    def __del__(self):
        """Ensure connection is closed when object is destroyed."""
        self.connection.close()