import logging
from typing import Dict, Any

def get_db_connection_details() -> Dict[str, Any]:
    """
    Retrieve and display database connection details for troubleshooting.
    Returns a dictionary containing connection information.
    """
    # Configure logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    try:
        # Get connection details from environment variables
        host = os.environ.get('DB_HOST')
        port = int(os.environ.get('DB_PORT', '5432'))
        db_name = os.environ.get('DB_NAME')
        user = os.environ.get('DB_USER')
        password = os.environ.get('DB_PASSWORD')

        # Validate required environment variables
        if not all([host, db_name, user]):
            raise ValueError("Missing required database environment variables")

        # Create and return connection details dictionary
        return {
            'host': host,
            'port': port,
            'database': db_name,
            'user': user,
            'password': password
        }

    except Exception as e:
        logger.error(f"Error retrieving database connection details: {str(e)}")
        raise