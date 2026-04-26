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

        # Verify KMS key exists
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

        # Prepare request
        operation = {
            'Action': 'SetAsPrimaryEncryptionContext',
            'KeyId': new_key_id,
            'Target': dataset_arn
        }

        # Execute change key operation
        response = kms_client.change_key_spec(**operation)
        
        # Verify operation was successful
        if response.get('KeyId') != new_key_id:
            logger.error("Failed to change key")
            return False

        logger.info("Successfully changed encryption key")
        return True

    except ClientError as e:
        logger.error(f"AWS error: {str(e)}")
        return False
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return False

def main():
    """Main function with example usage"""
    try:
        # Get credentials from environment variables
        kms_client = get_kms_client()
        
        # Example usage
        dataset_arn = os.environ.get('DATASET_ARN')
        new_key_id = os.environ.get('NEW_KEY_ID')
        
        if not all([dataset_arn, new_key_id]):
            logger.error("Missing required environment variables")
            return

        result = change_key_for_large_dataset(
            dataset_arn=dataset_arn,
            new_key_id=new_key_id,
            kms_client=kms_client
        )
        
        logger.info(f"Operation result: {result}")
        
    except Exception as e:
        logger.error(f"Error in main: {str(e)}")

if __name__ == "__main__":
    main()