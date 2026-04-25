import logging
from typing import Optional

def get_db_connection_details() -> Optional[dict]:
    """
    Retrieve database connection details for troubleshooting.
    Returns None if no connection is found.
    """
    try:
        # Get database connection
        db_connection = get_db_connection()
        
        # Get connection details
        connection_details = db_connection.get_connection_details()
        
        # Log connection details (without sensitive information)
        logging.info(f"Database connection established. Connection ID: {connection_details['connection_id']}")
        
        return connection_details
        
    except Exception as e:
        logging.error(f"Error retrieving database connection details: {str(e)}")
        return None