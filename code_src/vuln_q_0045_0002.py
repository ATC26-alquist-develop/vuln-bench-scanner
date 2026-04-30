```python
import logging
from typing import Optional
from contextlib import contextmanager
from psycopg2 import OperationalError
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Load environment variables from .env file
load_dotenv()

@contextmanager
def get_db_connection() -> Optional[tuple]:
    """
    Context manager for database connections.
    Returns a tuple of (connection, cursor) or None if connection fails.
    """
    try:
        # Get connection parameters from environment variables
        db_params = {
            'dbname': os.getenv('DB_NAME'),
            'user': os.getenv('DB_USER'),
            'password': os.getenv('DB_PASSWORD'),
            'host': os.getenv('DB_HOST'),
            'port': os.getenv('DB_PORT')
        }

        # Validate required parameters
        if not all(db_params.values()):
            logger.error("Missing database connection parameters")
            raise ValueError("Missing database connection parameters")

        # Create connection and cursor
        with psycopg2.connect(**db_params) as conn:
            with conn.cursor() as cur:
                yield conn, cur

    except OperationalError as e:
        logger.error(f"Database connection error: {e}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return None

def get_connection_details() -> None:
    """
    Retrieve and display database connection details for troubleshooting.
    """
    try:
        with get_db_connection() as (conn, cur):
            if conn is None:
                logger.error("Failed to establish database connection")
                return

            # Get connection details
            conn_params = conn.get_dsn_parameters()
            logger.info(f"Database connection details: {conn_params}")

            # Get current database name
            cur.execute("SELECT datname FROM pg_database WHERE datname = current_database()")
            db_name = cur.fetchone()
            logger.info(f"Current database: {db_name[0] if db_name else 'Unknown'}")

    except Exception as e:
        logger.error(f"Error retrieving connection details: {e}")
```