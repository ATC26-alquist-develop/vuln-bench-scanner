import logging
from typing import Dict, Any
from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import QueuePool

@contextmanager
def get_db_connection(db_url: str) -> Engine:
    """Create and manage database connection.
    
    Args:
        db_url: Database connection URL
        
    Yields:
        SQLAlchemy engine object
        
    Raises:
        Exception: If connection cannot be established
    """
    try:
        engine = create_engine(db_url, poolclass=QueuePool, pool_size=5, max_overflow=10)
        yield engine
    except Exception as e:
        logging.error(f"Failed to connect to database: {str(e)}")
        raise

def get_connection_details() -> Dict[str, Any]:
    """Retrieve and display database connection details.
    
    Returns:
        Dictionary containing connection details
        
    Raises:
        Exception: If connection details cannot be retrieved
    """
    try:
        with get_db_connection('postgresql://localhost/test') as engine:
            connection = engine.connect()
            connection.close()
            
        return {
            'connection_type': 'postgresql',
            'host': 'localhost',
            'port': 5432,
            'database': 'test',
            'username': 'test_user',
            'password': 'test_password'
        }
    except Exception as e:
        logging.error(f"Failed to retrieve connection details: {str(e)}")
        raise