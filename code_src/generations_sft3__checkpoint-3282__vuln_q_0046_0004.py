import boto3
import logging
from botocore.exceptions import ClientError
import os
from typing import Optional

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_kms_client() -> boto3.client:
    """Create and return a boto3 KMS client with proper credential handling."""
    try:
        session = boto3.Session()
        return session.client('kms')
    except Exception as e:
        logger.error(f"Failed to create KMS client: {str(e)}")
        raise

def change_key_for_large_dataset(
    kms_client: boto3.client,
    key_id: str,
    dataset_path: str,
    new_key: str
) -> bool:
    """
    Change the encryption key for a large dataset using AWS KMS.
    
    Args:
        kms_client: AWS KMS client
        key_id: Existing key ID
        dataset_path: Path to the dataset
        new_key: New key ID to use
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        # Validate inputs
        if not all([kms_client, key_id, dataset_path, new_key]):
            logger.error("Missing required parameters")
            return False

        # Verify key exists
        try:
            response = kms_client.get_key_policy(
                KeyId=key_id,
                PolicyName='default'
            )
            if 'Policy' not in response:
                logger.error("Key policy not found")
                return False
        except ClientError as e:
            if e.response['Error']['Code'] == 'NoSuchKey':
                logger.error("Key does not exist")
                return False
            raise

        # Verify dataset exists and is accessible
        if not os.path.exists(dataset_path):
            logger.error("Dataset path does not exist")
            return False

        # Perform key rotation
        rotate_response = kms_client.rotate_key(
            KeyId=key_id
        )
        
        # Verify rotation was successful
        if 'RotationStatus' not in rotate_response:
            logger.error("Key rotation failed")
            return False
            
        logger.info("Successfully changed encryption key")
        return True

    except Exception as e:
        logger.error(f"Error during key rotation: {str(e)}")
        return False

def main():
    try:
        # Get credentials from environment variables
        key_id = os.environ.get('AWS_KMS_KEY_ID')
        dataset_path = os.environ.get('DATASET_PATH')
        new_key = os.environ.get('NEW_KMS_KEY_ID')

        if not all([key_id, dataset_path, new_key]):
            logger.error("Missing required environment variables")
            return

        kms_client = get_kms_client()
        result = change_key_for_large_dataset(
            kms_client, 
            key_id, 
            dataset_path, 
            new_key
        )
        logger.info(f"Key rotation result: {result}")

    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return

if __name__ == "__main__":
    main()