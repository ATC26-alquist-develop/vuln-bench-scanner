import logging
from typing import Dict, Any

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_connection_details() -> Dict[str, Any]:
    """
    Retrieve and display database connection details for troubleshooting.
    Returns a dictionary containing connection information.
    """
    try:
        # Get connection details from environment variables
        host = os.environ.get('DB_HOST', 'localhost')
        port = int(os.environ.get('DB_PORT', '5432'))
        database = os.environ.get('DB_NAME')
        user = os.environ.get('DB_USER')
        password = os.environ.get('DB_PASSWORD')

        # Create connection details dictionary
        connection_details = {
            'Host': host,
            'Port': port,
            'Database': database,
            'User': user,
            'Password': '*' * len(password)  # Mask password
        }

        # Log connection details
        logger.info(f"Connection details retrieved:")
        for key, value in connection_details.items():
            logger.info(f"{key}: {value}")

        return connection_details

    except Exception as e:
        logger.error(f"Error retrieving connection details: {str(e)}")
        raise