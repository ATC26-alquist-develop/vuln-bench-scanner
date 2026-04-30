import boto3
import os
import logging
from botocore.exceptions import ClientError
from typing import Optional

def change_encryption_key(
    kms_client: boto3.client,
    source_key_id: str,
    destination_key_id: str,
    source_arn: str,
    destination_arn: str,
    kms_providers: Optional[list] = None
) -> bool:
    """
    Safely change encryption key for a dataset using AWS KMS.
    
    Args:
        kms_client: Initialized boto3 KMS client
        source_key_id: Current key ID to be replaced
        destination_key_id: New key ID to use
        source_arn: Source resource ARN
        destination_arn: Destination resource ARN
        kms_providers: List of KMS providers to use (default: all)
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        # Validate inputs
        if not all([kms_client, source_key_id, destination_key_id, source_arn, destination_arn]):
            logging.error("Missing required parameters")
            return False
            
        if not kms_providers:
            kms_providers = ['aws:kms']
            
        # Verify current key exists
        kms_client.describe_key(KeyId=source_key_id, Providers=kms_providers)
        
        # Verify new key exists
        kms_client.describe_key(KeyId=destination_key_id, Providers=kms_providers)
        
        # Perform key replacement
        kms_client.replace_key(
            KeyId=source_key_id,
            TargetKeyId=destination_key_id,
            SourceKeyId=source_key_id,
            PendingWindowInSeconds=3600,  # 1 hour
            Providers=kms_providers
        )
        
        # Wait for key rotation to complete
        waiter = kms_client.get_waiter('key_rotation_completed')
        waiter.wait(
            TargetKeyId=destination_key_id,
            Providers=kms_providers
        )
        
        return True
        
    except ClientError as e:
        logging.error(f"AWS KMS error: {str(e)}")
        return False
    except Exception as e:
        logging.error(f"Unexpected error: {str(e)}")
        return False