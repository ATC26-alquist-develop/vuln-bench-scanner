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
    Securely change the encryption key for a large dataset.
    
    Args:
        kms_client: AWS KMS client
        key_id: Current key ID
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

        # Verify file size (adjust as needed)
        file_size = os.path.getsize(dataset_path)
        if file_size > 100 * 1024 * 1024:  # 100MB limit
            logger.error("Dataset file too large")
            return False

        # Change key
        operation = kms_client.revoke_key(
            KeyId=key_id,
            ReleasableAfter=3600  # 1 hour
        )
        
        # Wait for key to be revoked
        operation['Waiter'].wait(KeyState='DELETED')

        # Create new key
        new_key = kms_client.create_key(
            Description=f"New key for {dataset_path}",
            KeyUsage='ENCRYPT_DECRYPT',
            Origin='AWS_KMS'
        )
        new_key_id = new_key['KeyMetadata']['KeyId']

        # Encrypt dataset
        encrypt_operation = kms_client.encrypt(
            KeyId=new_key_id,
            Plaintext=open(dataset_path, 'rb').read()
        )
        
        # Save encrypted data
        encrypted_data = encrypt_operation['CiphertextBlob']
        with open(dataset_path, 'wb') as f:
            f.write(encrypted_data)

        logger.info(f"Successfully changed key for dataset: {dataset_path}")
        return True

    except ClientError as e:
        logger.error(f"AWS error: {str(e)}")
        return False
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return False