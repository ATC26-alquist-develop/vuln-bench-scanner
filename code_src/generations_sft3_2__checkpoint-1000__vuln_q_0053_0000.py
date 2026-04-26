import os
import boto3
from botocore.exceptions import ClientError
import logging
from typing import Dict, Any

def get_secret() -> Dict[str, Any]:
    try:
        # Use environment variables for sensitive data
        secret_name = os.environ.get('SECRET_NAME')
        region_name = os.environ.get('AWS_REGION')

        if not secret_name or not region_name:
            raise ValueError("Missing required environment variables")

        # Initialize Secrets Manager client
        session = boto3.Session()
        client = session.client(
            service_name='secretsmanager',
            region_name=region_name
        )

        # Get secret value
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )

        # Return secret as dictionary
        return get_secret_value_response['SecretString']

    except ClientError as e:
        logging.error(f"Error accessing Secrets Manager: {str(e)}")
        raise
    except Exception as e:
        logging.error(f"Unexpected error: {str(e)}")
        raise