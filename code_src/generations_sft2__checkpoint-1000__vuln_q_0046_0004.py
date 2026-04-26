import boto3
import os
from botocore.exceptions import ClientError
from typing import Optional
import logging

def change_encryption_key(
    kms_client: boto3.client,
    source_key_id: str,
    destination_key_id: str,
    source_arn: str,
    destination_arn: str,
    kms_key: str
) -> Optional[dict]:
    """
    Securely change the encryption key for a dataset using AWS KMS.
    
    Args:
        kms_client: Boto3 KMS client
        source_key_id: Current key ID
        destination_key_id: New key ID
        source_arn: Source resource ARN
        destination_arn: Destination resource ARN
        kms_key: KMS key ARN
    
    Returns:
        Dict with operation details or None if operation fails
    """
    # Configure logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    try:
        # Validate inputs
        if not all([kms_client, source_key_id, destination_key_id, source_arn, destination_arn, kms_key]):
            logger.error("Missing required parameters")
            return None

        # Verify KMS key exists
        kms_client.get_key(key_id=kms_key)
        
        # Verify source key exists
        kms_client.get_key(key_id=source_key_id)
        
        # Verify destination key exists
        kms_client.get_key(key_id=destination_key_id)

        # Get current key alias
        alias_response = kms_client.describe_key(alias=source_key_id)
        current_alias = alias_response['KeyAlias']

        # Create new alias
        kms_client.create_alias(
            TargetKeyId=destination_key_id,
            TargetKeyAlias=current_alias
        )

        # Copy key
        kms_client.copy_key(
            SourceKeyId=source_key_id,
            KeyId=destination_key_id,
            SourceKeyArn=source_arn,
            KeyUsage='ENCRYPT_DECRYPT',
            Tags=[
                {
                    'Key': 'Purpose',
                    'Value': 'DataEncryption'
                }
            ]
        )

        # Update alias
        kms_client.update_alias(
            TargetKeyId=destination_key_id,
            TargetKeyAlias=current_alias
        )

        logger.info("Key change completed successfully")
        return {
            'status': 'success',
            'message': 'Key change completed successfully'
        }

    except ClientError as e:
        logger.error(f"AWS KMS error: {str(e)}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return None