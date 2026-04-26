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
    """Securely create and return a KMS client."""
    try:
        return boto3.client('kms')
    except Exception as e:
        logger.error(f"Failed to create KMS client: {str(e)}")
        raise

def change_key_for_large_dataset(
    dataset_id: str,
    new_key_id: str,
    kms_client: boto3.client,
    max_retries: int = 3
) -> bool:
    """
    Securely change the encryption key for a large dataset.
    
    Args:
        dataset_id: Unique identifier for the dataset
        new_key_id: New KMS key ID
        kms_client: Boto3 KMS client
        max_retries: Maximum number of retry attempts
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        # Validate inputs
        if not all([dataset_id, new_key_id]):
            logger.error("Invalid input parameters")
            return False
            
        # Validate dataset_id format
        if not isinstance(dataset_id, str) or not dataset_id.strip():
            logger.error("Invalid dataset_id format")
            return False
            
        # Validate new_key_id format
        if not isinstance(new_key_id, str) or not new_key_id.strip():
            logger.error("Invalid new_key_id format")
            return False

        # Get current key ID
        current_key_id = get_current_key_id(dataset_id, kms_client)
        if not current_key_id:
            logger.error("Failed to get current key ID")
            return False

        # Verify key rotation status
        if not is_key_rotated(current_key_id, new_key_id, kms_client):
            logger.error("Key rotation not allowed")
            return False

        # Perform key rotation
        rotate_key(dataset_id, new_key_id, kms_client)

        logger.info(f"Successfully changed key for dataset: {dataset_id}")
        return True

    except ClientError as e:
        logger.error(f"KMS client error: {str(e)}")
        return False
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return False

def get_current_key_id(dataset_id: str, kms_client: boto3.client) -> Optional[str]:
    """Get the current key ID for the dataset."""
    try:
        # Use a consistent prefix for dataset IDs
        prefix = "dataset_"
        if not dataset_id.startswith(prefix):
            dataset_id = f"{prefix}{dataset_id}"
            
        paginator = kms_client.get_paginator('list_keys')
        for page in paginator.paginate():
            for key in page.get('Keys', []):
                if key.get('KeyId') == dataset_id:
                    return key.get('KeyId')
        return None
    except Exception as e:
        logger.error(f"Failed to get current key ID: {str(e)}")
        return None

def is_key_rotated(current_key_id: str, new_key_id: str, kms_client: boto3.client) -> bool:
    """Check if key rotation is allowed."""
    try:
        # Verify the new key is not the current key
        if new_key_id == current_key_id:
            logger.error("Cannot rotate to the same key")
            return False
            
        # Verify the new key is not expired
        paginator = kms_client.get_paginator('list_keys')
        for page in paginator.paginate():
            for key in page.get('Keys', []):
                if key.get('KeyId') == new_key_id:
                    if key.get('KeyState') != 'Enabled':
                        logger.error("New key is not