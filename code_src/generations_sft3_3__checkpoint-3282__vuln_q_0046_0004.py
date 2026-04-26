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
    """Create and return a secure KMS client"""
    try:
        return boto3.client('kms')
    except Exception as e:
        logger.error(f"Failed to create KMS client: {str(e)}")
        raise

def change_key_for_large_dataset(
    kms_client: boto3.client,
    key_id: str,
    dataset_path: str,
    new_key_id: str
) -> bool:
    """
    Securely change encryption key for a large dataset
    
    Args:
        kms_client: KMS client
        key_id: Current key ID
        dataset_path: Path to dataset
        new_key_id: New key ID
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        # Validate inputs
        if not all([kms_client, key_id, dataset_path, new_key_id]):
            logger.error("Missing required parameters")
            return False

        # Verify dataset exists and is accessible
        if not os.path.exists(dataset_path):
            logger.error("Dataset path does not exist")
            return False

        # Verify KMS key exists and is enabled
        try:
            kms_client.get_key_policy(
                KeyId=key_id,
                PolicyName='default'
            )
        except ClientError as e:
            if e.response['Error']['Code'] == 'NoSuchKey':
                logger.error("Invalid key ID")
                return False
            raise

        # Verify new key exists and is enabled
        try:
            kms_client.get_key_policy(
                KeyId=new_key_id,
                PolicyName='default'
            )
        except ClientError as e:
            if e.response['Error']['Code'] == 'NoSuchKey':
                logger.error("Invalid new key ID")
                return False
            raise

        # Perform key rotation
        try:
            response = kms_client.revoke_key(
                KeyId=key_id,
                RevokeAllPermissions=True
            )
            logger.info("Current key revoked")

            response = kms_client.create_key(
                KeyUsage='ENCRYPT_DECRYPT',
                Origin='AWS_KMS',
                Description='Rotated key for large dataset'
            )
            new_key_id = response['KeyMetadata']['KeyId']
            logger.info("New key created")

            response = kms_client.import_key_material(
                KeyId=new_key_id,
                CryptographicOperation='ENCRYPT_DECRYPT',
                CryptographicSource='USER_PASSWORD'
            )
            logger.info("New key material imported")

            # Update dataset encryption
            with open(dataset_path, 'rb') as dataset:
                data = dataset.read()
                encrypted_data = kms_client.encrypt(
                    KeyId=new_key_id,
                    Plaintext=data
                )['CiphertextBlob']

            # Write encrypted data back
            with open(dataset_path, 'wb') as dataset:
                dataset.write(encrypted_data)

            logger.info("Dataset encrypted with new key")
            return True

        except ClientError as e:
            logger.error(f"Failed to change key: {str(e)}")
            return False

    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return False

def main():
    # Example usage with environment variables for sensitive data
    try:
        kms_client = get_kms_client()
        key_id = os.environ.get('KMS_KEY_ID')
        dataset_path = os.environ.get('DATASET_PATH')
        new_key_id = os.environ.get('NEW_KMS_KEY_ID')

        if not all([key_id, dataset_path, new_key_id]):
            logger.error("Missing required environment variables")
            return

        success = change_key