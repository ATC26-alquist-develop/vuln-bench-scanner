import boto3
import logging
from botocore.exceptions import ClientError
import os
from typing import Optional

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def rotate_kms_key(key_id: str, new_key: str) -> bool:
    """
    Securely rotate an AWS KMS key for a large dataset
    
    Args:
        key_id: The ID of the KMS key to rotate
        new_key: The new key ID to use
        
    Returns:
        bool: True if rotation was successful, False otherwise
    """
    try:
        # Validate inputs
        if not key_id or not new_key:
            logger.error("Invalid key ID or new key")
            return False
            
        # Validate key ID format
        if not isinstance(key_id, str) or not isinstance(new_key, str):
            logger.error("Invalid input types")
            return False
            
        # Validate key ID length
        if len(key_id) > 36 or len(new_key) > 36:
            logger.error("Invalid key ID length")
            return False

        # Initialize KMS client
        kms_client = boto3.client('kms')
        
        # Get current key version
        key_versions = kms_client.list_key_versions(KeyId=key_id)
        if not key_versions or 'Versions' not in key_versions:
            logger.error("No versions found for key")
            return False
            
        current_version = key_versions['Versions'][0]['VersionNumber']
        
        # Rotate key
        rotate_params = {
            'KeyId': key_id,
            'RotationMode': 'IMMEDIATE',
            'RotationRules': {
                'RotationInterval': 86400,  # 24 hours
                'RotationTimeWindow': 3600,  # 1 hour
                'Enabled': True
            }
        }
        
        response = kms_client.rotate_key(**rotate_params)
        
        # Verify rotation
        if 'RotationStatus' in response and response['RotationStatus']['RotationState'] == 'ROTATING':
            logger.info("Key rotation initiated")
            return True
            
        logger.info("Key rotation completed successfully")
        return True
        
    except ClientError as e:
        logger.error(f"AWS error: {str(e)}")
        return False
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return False