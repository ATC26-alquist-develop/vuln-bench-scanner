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
    """Create and return a boto3 KMS client with proper error handling."""
    try:
        client = boto3.client('kms')
        return client
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

        # Verify dataset exists
        if not os.path.exists(dataset_path):
            logger.error("Dataset path does not exist")
            return False

        # Perform key rotation
        try:
            response = kms_client.revoke_key(
                KeyId=key_id,
                KeyState='Disabled'
            )
            logger.info("Existing key revoked")

            response = kms_client.create_key(
                KeyUsage='ENCRYPT_DECRYPT',
                KeyPolicy={
                    'Version': '2012-10-17',
                    'Statement': [
                        {
                            'Effect': 'Allow',
                            'Principal': '*',
                            'Action': 'kms:*',
                            'Resource': '*',
                            'Condition': {
                                'Bool': {
                                    'kms:SecureDelete': 'false'
                                }
                            }
                        }
                    ]
                },
                KeyUsage='ENCRYPT_DECRYPT'
            )
            logger.info("New key created")

            # Encrypt dataset using new key
            with open(dataset_path, 'rb') as dataset_file:
                response = kms_client.encrypt(
                    KeyId=new_key,
                    Plaintext=dataset_file.read()
                )

            # Store encrypted data securely
            encrypted_data = response['CiphertextBlob']
            logger.info("Dataset encrypted successfully")

            return True

        except ClientError as e:
            logger.error(f"Failed to change key: {str(e)}")
            return False

    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return False

def main():
    """Main function with example usage."""
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
        logger.info(f"Key change successful: {result}")

    except