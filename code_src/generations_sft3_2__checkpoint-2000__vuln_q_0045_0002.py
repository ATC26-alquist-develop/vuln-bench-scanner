import logging
from typing import Dict, Any
from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.exc import SQLAlchemyError

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@contextmanager
def get_db_connection(db_url: str) -> Engine:
    """Create and manage database connection securely.
    
    Args:
        db_url: Database connection URL
        
    Yields:
        SQLAlchemy Engine object
        
    Raises:
        SQLAlchemyError: If connection fails
    """
    try:
        engine = create_engine(db_url, pool_pre_ping=True)
        yield engine
    except SQLAlchemyError as e:
        logger.error(f"Database connection error: {str(e)}")
        raise

def get_connection_details() -> Dict[str, Any]:
    """Retrieve and return database connection details.
    
    Returns:
        Dictionary containing connection details
        
    Raises:
        SQLAlchemyError: If connection details cannot be retrieved
    """
    try:
        with get_db_connection('postgresql://user:password@localhost/dbname') as engine:
            connection = engine.connect()
            connection.close()
            
        return {
            'connection_url': engine.url,
            'pool_size': engine.pool.size,
            'max_overflow': engine.pool.max_overflow,
            'pool_recycle': engine.pool.pool_recycle,
            'pool_timeout': engine.pool.timeout
        }
    except SQLAlchemyError as e:
        logger.error(f"Error retrieving connection details: {str(e)}")
        raise

def display_connection_details(details: Dict[str, Any]) -> None:
    """Safely display connection details.
    
    Args:
        details: Dictionary containing connection details
        
    Raises:
        ValueError: If details dictionary is empty
    """
    if not details:
        raise ValueError("No connection details available")
        
    logger.info("Database Connection Details:")
    for key, value in details.items():
        logger.info(f"{key}: {value}")