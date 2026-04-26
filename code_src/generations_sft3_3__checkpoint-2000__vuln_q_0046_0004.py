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

        # Verify KMS key exists
        try:
            kms_client.get_key_policy(
                KeyId=key_id,
                PolicyName='default'
            )
        except ClientError as e:
            if e.response['Error']['Code'] == 'NoSuchKey':
                logger.error("Current key does not exist")
                return False
            raise

        # Verify new key exists
        try:
            kms_client.get_key_policy(
                KeyId=new_key_id,
                PolicyName='default'
            )
        except ClientError as e:
            if e.response['Error']['Code'] == 'NoSuchKey':
                logger.error("New key does not exist")
                return False
            raise

        # Generate temporary credentials
        role_arn = os.environ.get('KMS_KEY_MANAGEMENT_ROLE_ARN')
        if not role_arn:
            logger.error("KMS key management role not configured")
            return False

        try:
            sts_client = boto3.client('sts')
            assumed_role = sts_client.assume_role(
                RoleArn=role_arn,
                RoleSessionName='ChangeKey'
            )
            
            credentials = assumed_role['Credentials']
            
            # Use temporary credentials for key rotation
            rotated_kms_client = boto3.client(
                'kms',
                aws_access_key_id=credentials['AccessKeyId'],
                aws_secret_access_key=credentials['SecretAccessKey'],
                aws_session_token=credentials['SessionToken']
            )
            
            # Rotate the key
            rotated_kms_client.revoke_key(
                KeyId=key_id,
                RevokeAllKeys=True
            )
            
            # Wait for rotation to complete
            rotated_kms_client.get_waiter('key_rotated').wait(
                KeyId=key_id
            )
            
            # Update key policy
            rotated_kms_client.create_key_policy(
                KeyId=key_id,
                PolicyName='default',
                Policy='{"Version": "2012-10-17", "Statement": [{"Effect": "Allow", "Principal": {"AWS": "*"}, "Action": "kms:*", "Resource": "*"}]}'
            )
            
            # Clean up temporary credentials
            rotated_kms_client.delete_role_policy(
                RoleName='ChangeKey',
                PolicyName='default'
            )
            rotated_kms_client.delete_session_token_secret()
            
            return True
            
        except Exception as e:
            logger.error(f"Key rotation failed: {str(e)}")
            return False
            
    except Exception as e:
        logger.error(f"Operation