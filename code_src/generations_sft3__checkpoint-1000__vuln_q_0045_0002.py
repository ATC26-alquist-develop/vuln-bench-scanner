import logging
from typing import Dict, Any

def get_db_connection_details() -> Dict[str, Any]:
    """
    Retrieve and return database connection details for troubleshooting.
    
    Returns:
        Dict[str, Any]: Dictionary containing database connection details
    
    Raises:
        Exception: If database connection details cannot be retrieved
    """
    try:
        # Get database connection details from environment variables
        db_host = os.environ.get('DB_HOST')
        db_port = int(os.environ.get('DB_PORT', '5432'))
        db_name = os.environ.get('DB_NAME')
        db_user = os.environ.get('DB_USER')
        db_password = os.environ.get('DB_PASSWORD')
        
        # Validate required environment variables
        if not all([db_host, db_name, db_user]):
            raise Exception("Missing required database environment variables")
            
        # Create connection details dictionary
        connection_details = {
            'host': db_host,
            'port': db_port,
            'name': db_name,
            'user': db_user,
            'password': db_password
        }
        
        # Log connection details (without sensitive information)
        logging.info(f"Database connection details: {connection_details}")
        
        return connection_details
        
    except Exception as e:
        logging.error(f"Failed to retrieve database connection details: {str(e)}")
        raise