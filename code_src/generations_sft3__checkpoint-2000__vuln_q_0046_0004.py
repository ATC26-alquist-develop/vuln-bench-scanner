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
    dataset_arn: str,
    new_key_id: str,
    kms_client: boto3.client
) -> bool:
    """
    Securely change encryption key for a large dataset
    
    Args:
        dataset_arn: ARN of the dataset
        new_key_id: New KMS key ID
        kms_client: AWS KMS client
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        # Validate inputs
        if not all([dataset_arn, new_key_id, kms_client]):
            logger.error("Missing required parameters")
            return False

        # Verify dataset exists
        try:
            kms_client.get_key_policy(
                KeyId=dataset_arn,
                PolicyName='default'
            )
        except ClientError as e:
            if e.response['Error']['Code'] == 'NoSuchKey':
                logger.error("Dataset ARN not found")
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
                logger.error("New key not found")
                return False
            raise

        # Change key policy
        kms_client.update_key_policy(
            KeyId=dataset_arn,
            PolicyName='default',
            Statement=[{
                'Effect': 'Allow',
                'Principal': {'AWS': '*'},
                'Action': 'kms:Encrypt',
                'Resource': '*',
                'Condition': {
                    'StringEquals': {
                        f"kms:CallerKeyId/{dataset_arn}": new_key_id
                    }
                }
            }]
        )

        logger.info(f"Successfully changed key for dataset {dataset_arn}")
        return True

    except ClientError as e:
        logger.error(f"AWS error: {str(e)}")
        return False
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return False