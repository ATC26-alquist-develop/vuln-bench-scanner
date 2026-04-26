```python
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
    Change encryption key for a large dataset using AWS KMS.
    
    Args:
        kms_client: KMS client
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
            kms_client.get_key_policy(
                KeyId=key_id,
                PolicyName='default'
            )
        except ClientError as e:
            if e.response['Error']['Code'] == 'NoSuchKey':
                logger.error(f"Key {key_id} does not exist")
                return False
            raise

        # Verify new key exists
        try:
            kms_client.get_key_policy(
                KeyId=new_key,
                PolicyName='default'
            )
        except ClientError as e:
            if e.response['Error']['Code'] == 'NoSuchKey':
                logger.error(f"New key {new_key} does not exist")
                return False
            raise

        # Get current key material
        try:
            current_key_material = kms_client.get_key_rotation_status(
                KeyId=key_id
            )['KeyRotationEnabled']
        except ClientError as e:
            logger.error(f"Failed to get key rotation status: {str(e)}")
            return False

        # Change key
        try:
            kms_client.change_key_spec(
                KeyId=key_id,
                KeySpec='AES_256'
            )
            logger.info(f"Successfully changed key specification for {key_id}")
            
            # Rotate key
            if current_key_material:
                kms_client.schedule_key_rotation(
                    KeyId=key_id
                )
                logger.info(f"Scheduled rotation for {key_id}")
            
            # Rotate key
            if current_key_material:
                kms_client.rotate_key(
                    KeyId=key_id
                )
                logger.info(f"Rotated key for {key_id}")
            
            return True
            
        except ClientError as e:
            logger.error(f"Failed to change key: {str(e)}")
            return False

    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
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
        logger.info(f"Key change result: {result}")
        
    except Exception as e:
        logger.error(f"Error in main execution: {str(e)}