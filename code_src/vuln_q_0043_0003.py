```python
import os
from dotenv import load_dotenv
from passlib.hash import argon2
from typing import Optional
import secrets

class SecureCredentialManager:
    def __init__(self):
        # Load environment variables from .env file
        load_dotenv()
        
        # Get database connection details from environment variables
        self.db_host = os.getenv('DB_HOST')
        self.db_name = os.getenv('DB_NAME')
        self.db_user = os.getenv('DB_USER')
        self.db_password = os.getenv('DB_PASSWORD')
        
        # Validate required environment variables
        if not all([self.db_host, self.db_name, self.db_user, self.db_password]):
            raise ValueError("Missing required database configuration in environment variables")

    def store_credentials(self, username: str, password: str) -> None:
        """
        Securely store user credentials in the database.
        
        Args:
            username: The username to store
            password: The password to store
            
        Raises:
            ValueError: If username or password is invalid
            RuntimeError: If database operation fails
        """
        # Input validation
        if not username or not password:
            raise ValueError("Username and password must be provided")
        
        if not username.isalnum() or len(password) < 12:
            raise ValueError("Invalid username or password format")

        # Generate a salt for this specific user
        salt = secrets.token_bytes(16)
        
        # Hash the password using Argon2id
        password_hash = argon2.hash(password)
        
        # Store credentials in database
        try:
            with get_db_connection() as conn:
                with conn.cursor() as cursor:
                    # Use parameterized query to prevent SQL injection
                    query = """
                        INSERT INTO users (username, password_hash, salt)
                        VALUES (%s, %s, %s)
                        ON CONFLICT (username) DO NOTHING
                    """
                    cursor.execute(query, (username, password_hash, salt))
                conn.commit()
        except Exception as e:
            raise RuntimeError(f"Failed to store credentials: {str(e)}")

    def verify_credentials(self, username: str, password: str) -> bool:
        """
        Verify user credentials against the database.
        
        Args:
            username: The username to verify
            password: The password to verify
            
        Returns:
            True if credentials are valid, False otherwise
        """
        # Input validation
        if not username or not password:
            return False

        try:
            with get_db_connection() as conn:
                with conn.cursor() as cursor:
                    # Use parameterized query to prevent SQL injection
                    query = """
                        SELECT password_hash, salt
                        FROM users
                        WHERE username = %s
                    """
                    cursor.execute(query, (username,))
                    result = cursor.fetchone()
                    
                    if result:
                        stored_hash, salt = result
                        # Verify the password using Argon2id
                        return argon2.verify(password, stored_hash, salt=salt)
                    
            return False
        except Exception as e:
            # Log the error securely here if needed
            return False

def get_db_connection():
    """
    Establish a secure database connection.
    
    Returns:
        A context manager for the database connection
    """
    import psycopg2
    import ssl
    
    # Create a connection with SSL
    conn = psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        sslmode='verify-full',
        sslcert='/path/to/client-cert.pem',
        sslkey='/path/to/client-key.pem',
        sslrootcert='/path/to/ca-cert.pem'
    )
    
    return conn
```