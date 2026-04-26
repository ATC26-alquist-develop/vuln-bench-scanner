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
    """Retrieve and display database connection details.
    
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
            'connection_type': 'postgresql',
            'host': 'localhost',
            'port': 5432,
            'database': 'dbname',
            'user': 'user',
            'password': 'password'
        }
    except SQLAlchemyError as e:
        logger.error(f"Failed to retrieve connection details: {str(e)}")
        raise

def main():
    try:
        details = get_connection_details()
        logger.info("Connection details:")
        for key, value in details.items():
            logger.info(f"{key}: {value}")
    except Exception as e:
        logger.error(f"Error in main function: {str(e)}")

if __name__ == "__main__":
    main()