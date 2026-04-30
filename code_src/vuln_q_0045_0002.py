import logging
from typing import Optional

def get_db_connection_details() -> Optional[dict]:
    """
    Retrieve database connection details for troubleshooting purposes.
    
    Returns:
        dict: A dictionary containing database connection details if available, otherwise None.
    """
    # Configure logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    
    try:
        # Retrieve database connection details
        db_details = {
            'host': 'localhost',
            'port': 5432,
            'database': 'mydb',
            'user': 'myuser',
            'password': 'mypassword'
        }
        
        # Log the retrieved connection details
        logger.info("Retrieved database connection details")
        
        return db_details
    
    except Exception as e:
        # Log any exceptions that occur
        logger.error(f"Error retrieving database connection details: {str(e)}")
        return None