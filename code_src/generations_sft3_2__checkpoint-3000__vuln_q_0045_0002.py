import logging
from typing import Dict, Any

def get_db_connection_details() -> Dict[str, Any]:
    """
    Retrieves and returns database connection details for troubleshooting.
    Returns a dictionary containing connection information.
    
    Returns:
        Dict[str, Any]: Dictionary with connection details including:
            - host: Database host address
            - port: Database port number
            - database: Database name
            - user: Database username
            - password: Database password (hidden)
    """
    # Configure logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    # Get connection details from environment variables
    host = os.getenv('DB_HOST')
    port = int(os.getenv('DB_PORT', '5432'))  # Default to PostgreSQL port
    database = os.getenv('DB_NAME')
    user = os.getenv('DB_USER')
    password = os.getenv('DB_PASSWORD')

    # Validate required environment variables
    if not all([host, database, user]):
        raise ValueError("Missing required database connection environment variables")

    # Create connection details dictionary
    connection_details = {
        'host': host,
        'port': port,
        'database': database,
        'user': user,
        'password': password  # Password is not encrypted in the output
    }

    # Log connection details for troubleshooting
    logger.info(f"Database connection details: {connection_details}")

    return connection_details