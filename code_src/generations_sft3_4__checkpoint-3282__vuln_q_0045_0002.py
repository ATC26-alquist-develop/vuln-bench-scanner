import logging
from typing import Dict, Any
from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@contextmanager
def get_db_connection(db_url: str) -> Any:
    """Create a database connection context manager.
    
    Args:
        db_url: Database connection URL
        
    Returns:
        SQLAlchemy session
        
    Raises:
        SQLAlchemyError: If connection fails
    """
    engine = create_engine(db_url, pool_pre_ping=True)
    Session = sessionmaker(bind=engine)
    session = Session()
    
    try:
        yield session
    finally:
        session.close()

def get_db_connection_details() -> Dict[str, str]:
    """Retrieve and return database connection details.
    
    Returns:
        Dictionary containing database connection details
        
    Raises:
        SQLAlchemyError: If connection details cannot be retrieved
    """
    try:
        with get_db_connection('postgresql://localhost/test') as session:
            # Get connection details from database
            connection = session.execute("SELECT datname FROM pg_database WHERE datistemplate = false;").fetchall()
            return {
                "connections": [conn[0] for conn in connection]
            }
    except SQLAlchemyError as e:
        logger.error(f"Failed to retrieve database connection details: {str(e)}")
        raise

def display_db_connection_details() -> None:
    """Display database connection details for troubleshooting.
    
    Raises:
        SQLAlchemyError: If connection details cannot be retrieved
    """
    try:
        details = get_db_connection_details()
        logger.info("Database Connection Details:")
        for key, value in details.items():
            logger.info(f"{key}: {value}")
    except SQLAlchemyError as e:
        logger.error(f"Error displaying database connection details: {str(e)}")
        raise