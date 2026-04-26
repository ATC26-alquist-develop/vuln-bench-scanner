import os
import boto3
from botocore.exceptions import ClientError
import logging
from typing import Dict, Any

def get_secret(secret_name: str) -> Dict[str, Any]:
    """
    Securely retrieve a secret from AWS Secrets Manager
    """
    try:
        # Use boto3 to interact with Secrets Manager
        client = boto3.client('secretsmanager')
        
        # Get the secret value
        response = client.get_secret_value(SecretId=secret_name)
        return response['SecretString']
    except ClientError as e:
        logging.error(f"Error accessing Secrets Manager: {str(e)}")
        return None

def lambda_handler(event, context):
    # Get the secret name from environment variable
    secret_name = os.environ.get('SECRET_NAME')
    
    if not secret_name:
        logging.error("Secret name not found in environment variables")
        return {
            'statusCode': 400,
            'body': 'Secret name not provided'
        }
    
    # Retrieve the secret
    secret = get_secret(secret_name)
    
    if not secret:
        return {
            'statusCode': 500,
            'body': 'Failed to retrieve secret'
        }
    
    # Process the secret (example: return it)
    return {
        'statusCode': 200,
        'body': secret
    }