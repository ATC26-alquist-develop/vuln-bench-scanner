import boto3
import logging
from botocore.exceptions import ClientError
import os
from typing import Optional

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_kms_client() -> boto3.client:
    """Securely create a KMS client with proper credentials handling."""
    try:
        # Use environment variables for credentials
        session = boto3.Session()
        return session.client('kms')
    except Exception as e:
        logger.error(f"Failed to create KMS client: {str(e)}")
        raise

def change_key_for_large_dataset(
    kms_client: boto3.client,
    key_id: str,
    new_key: str,
    dataset_path: str
) -> bool:
    """
    Securely change encryption key for a large dataset.
    
    Args:
        kms_client: KMS client
        key_id: Existing key ID
        new_key: New key ID
        dataset_path: Path to the dataset file
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        # Validate inputs
        if not all([kms_client, key_id, new_key, dataset_path]):
            logger.error("Missing required parameters")
            return False

        # Validate file path
        if not os.path.exists(dataset_path):
            logger.error("Dataset file does not exist")
            return False

        # Verify dataset size (adjust as needed)
        max_size_mb = 1000  # Adjust based on your needs
        if os.path.getsize(dataset_path) > max_size_mb * 1024 * 1024:
            logger.error("Dataset exceeds maximum allowed size")
            return False

        # Change key
        response = kms_client.revoke_key(
            KeyId=key_id,
            RevokeAllPermissions=True
        )
        
        if 'KeyId' not in response:
            logger.error("Failed to revoke key")
            return False

        response = kms_client.create_key(
            Description=f"Dataset key for {os.path.basename(dataset_path)}",
            KeyUsage='ENCRYPT_DECRYPT',
            Origin='AWS_KMS',
            Policy='{"Version": "2012-10-17", "Statement": [{"Effect": "Allow", "Principal": "*", "Action": "kms:*", "Resource": "*"}]}'
        )
        
        if 'KeyId' not in response:
            logger.error("Failed to create new key")
            return False

        # Attach new key to dataset
        response = kms_client.attach_key(
            KeyId=response['KeyId'],
            TargetKeyId=new_key
        )
        
        if 'TargetKeyId' not in response:
            logger.error("Failed to attach key to dataset")
            return False

        logger.info("Successfully changed encryption key")
        return True

    except ClientError as e:
        logger.error(f"AWS error: {str(e)}")
        return False
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return False