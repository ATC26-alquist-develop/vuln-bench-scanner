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

def get_db_connection_details() -> Dict[str, Any]:
    """Retrieve and display database connection details.
    
    Returns:
        Dictionary containing database connection details
        
    Raises:
        SQLAlchemyError: If connection fails
    """
    try:
        with get_db_connection('postgresql://localhost/test') as session:
            connection = session.connection()
            connection.execute("SELECT version();")
            version = connection.fetchone()[0]
            
            return {
                'version': version,
                'connection_url': 'postgresql://localhost/test',
                'connection_params': {
                    'host': 'localhost',
                    'port': '5432',
                    'database': 'test',
                    'user': 'test_user',
                    'password': 'test_password'
                }
            }
            
    except SQLAlchemyError as e:
        logger.error(f"Failed to connect to database: {str(e)}")
        raise

def main():
    try:
        details = get_db_connection_details()
        logger.info("Database connection details:")
        for key, value in details.items():
            logger.info(f"{key}: {value}")
    except Exception as e:
        logger.error(f"Error occurred: {str(e)}")

if __name__ == "__main__":
    main()