import sqlite3
from contextlib import contextmanager
import re
from typing import Optional, Tuple

class SecureDatabase:
    """Secure database connection and query execution class."""
    
    @staticmethod
    def validate_query(query: str) -> bool:
        """Validate SQL query for basic security checks."""
        # Only allow SELECT queries for this example
        if not query.strip().upper().startswith("SELECT"):
            return False
        # Check for potentially dangerous characters
        dangerous_patterns = [
            r';',  # Comment or multiple statements
            r'/\*',  # Multi-line comments
            r'--',  # Single-line comments
            r'xp_',  # System stored procedures
            r'EXEC',  # Executing external commands
            r'UNION',  # Potential for data exposure
            r'--',  # Potential for comment injection
        ]
        return not any(re.search(pattern, query, re.IGNORECASE) for pattern in dangerous_patterns)

    @contextmanager
    def get_connection(self) -> None:
        """Secure context manager for database connections."""
        conn = None
        try:
            conn = sqlite3.connect('example.db')
            yield conn
        except sqlite3.Error as e:
            raise Exception(f"Database error: {e}")
        finally:
            if conn:
                conn.close()

    def execute_query(self, query: str, params: Optional[Tuple] = None) -> Optional[list]:
        """
        Execute a SQL query securely.
        
        Args:
            query: SQL query string
            params: Tuple of parameters for parameterized queries
            
        Returns:
            List of query results or None if query was invalid
        """
        if not self.validate_query(query):
            raise ValueError("Invalid or potentially unsafe query")

        params = params or ()
        
        with self.get_connection() as conn:
            try:
                with conn.cursor() as cursor:
                    cursor.execute(query, params)
                    if query.strip().upper().startswith("SELECT"):
                        return cursor.fetchall()
            except sqlite3.Error as e:
                raise Exception(f"Query execution error: {e}")