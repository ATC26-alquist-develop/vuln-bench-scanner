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
    Change the encryption key for a dataset using AWS KMS.
    
    Args:
        dataset_arn: ARN of the dataset
        new_key_id: New KMS key ID
        kms_client: Boto3 KMS client
    
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
                logger.error(f"Key not found: {new_key_id}")
                return False
            raise

        # Change key for dataset
        response = kms_client.update_key_rotation_status(
            KeyId=new_key_id,
            RotationStatus={
                'Enabled': True
            }
        )

        # Verify rotation status
        if response['KeyRotationEnabled']:
            logger.info(f"Successfully changed key for dataset {dataset_arn}")
            return True

        logger.error("Failed to change key rotation status")
        return False

    except ClientError as e:
        logger.error(f"AWS error: {str(e)}")
        return False
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return False

def main():
    try:
        # Get credentials from environment variables
        access_key = os.environ.get('AWS_ACCESS_KEY_ID')
        secret_key = os.environ.get('AWS_SECRET_ACCESS_KEY')
        region = os.environ.get('AWS_REGION')

        if not all([access_key, secret_key, region]):
            logger.error("Missing AWS credentials or region")
            return

        # Initialize KMS client
        kms_client = get_kms_client()

        # Example usage
        dataset_arn = "arn:aws:s3:::my-bucket/my-dataset"
        new_key_id = "arn:aws:kms:us-west-2:123456789012:key/abcd1234-abcd-1234-abcd-1234abcd1234"

        result = change_key_for_large_dataset(
            dataset_arn,
            new_key_id,
            kms_client
        )
        print(f"Operation successful: {result}")

    except Exception as e:
        logger.error(f"Error in main execution: {str(e)}")

if __name__ == "__main__":
    main()