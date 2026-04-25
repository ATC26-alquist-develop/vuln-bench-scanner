import os
import re
from typing import Optional
import boto3
from botocore.exceptions import ClientError
from aws_cdk import core
from aws_cdk.core import Duration
from aws_cdk.core import Stack

class SecureS3BucketStack(Stack):
    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)
        
        # Validate bucket name
        if not self._validate_bucket_name(bucket_name):
            raise ValueError("Invalid bucket name format")
            
        # Create S3 bucket with secure settings
        bucket = self._create_secure_s3_bucket(bucket_name)
        
    def _validate_bucket_name(self, name: str) -> bool:
        """Validate bucket name format and restrictions"""
        if not isinstance(name, str):
            return False
        # Bucket name must be 3-63 chars, lowercase, and can only contain letters, numbers, dots, and hyphens
        pattern = r'^[a-z0-9][a-z0-9.-]{1,61}[a-z0-9]$'
        return bool(re.match(pattern, name.lower()))
        
    def _create_secure_s3_bucket(self, name: str) -> core.ICloudFormationResource:
        """Create S3 bucket with secure configuration"""
        try:
            # Use environment variables for credentials
            aws_region = os.environ.get('AWS_REGION', 'us-east-1')
            aws_access_key_id = os.environ.get('AWS_ACCESS_KEY_ID')
            aws_secret_access_key = os.environ.get('AWS_SECRET_ACCESS_KEY')
            
            if not all([aws_region, aws_access_key_id, aws_secret_access_key]):
                raise ValueError("AWS credentials not found in environment variables")
                
            # Create S3 client
            s3_client = boto3.client(
                's3',
                region_name=aws_region,
                aws_access_key_id=aws_access_key_id,
                aws_secret_access_key=aws_secret_access_key
            )
            
            # Create bucket with default encryption
            response = s3_client.create_bucket(
                Bucket=name,
                CreateBucketConfiguration={
                    'LocationConstraint': aws_region
                },
                ObjectLockEnabledForBucket=False,
                BucketEncryption={
                    'ServerSideEncryptionConfiguration': [{
                        'ServerSideEncryptionByDefault': {
                            'SSEAlgorithm': 'AES256'
                        }
                    }]
                }
            )
            
            # Wait for bucket to be created
            s3_client.get_bucket_encryption(
                Bucket=name
            )
            
            return response['LocationConstraint']
            
        except ClientError as e:
            raise ValueError(f"Failed to create S3 bucket: {str(e)}")
        except Exception as e:
            raise ValueError(f"Unexpected error creating S3 bucket: {str(e)}")

# Usage example:
# app = core.App()
# stack = SecureS3BucketStack(app, "SecureBucketStack", env=core.Environment(
#     region_name="us-west-2",
#     account_id="123456789012"
# ))
# stack.s3_bucket_name = "my-secure-bucket"
# app.synth()