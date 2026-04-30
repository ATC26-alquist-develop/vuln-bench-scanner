```python
import os
import logging
import boto3
import re
from aws_cdk import core
from aws_cdk import aws_s3 as s3

class SecureS3Bucket(core.Construct):
    def __init__(self, scope: core.Construct, id: str, bucket_name: str, **kwargs):
        super().__init__(scope, id)
        
        # Validate bucket name
        if not self._is_valid_bucket_name(bucket_name):
            raise ValueError("Invalid bucket name")
            
        # Get credentials from environment variables
        aws_access_key_id = os.environ.get('AWS_ACCESS_KEY_ID')
        aws_secret_access_key = os.environ.get('AWS_SECRET_ACCESS_KEY')
        aws_region = os.environ.get('AWS_REGION')
        
        if not all([aws_access_key_id, aws_secret_access_key, aws_region]):
            raise ValueError("Missing required AWS credentials")
            
        # Create S3 bucket with default security settings
        self.bucket = s3.Bucket(self, 
            'SecureBucket', 
            bucket_name=bucket_name,
            removal_policy=core.RemovalPolicy.DESTROY,  # Use with caution
            auto_delete_objects=True,  # Automatically delete objects on bucket deletion
            block_public_access=s3.BlockPublicAccess.BLOCK_ALL,  # Block all public access
            encryption=s3.BucketEncryption.S3_MANAGED,  # Enable default encryption
            versioning=s3.BucketVersioning.ENABLED  # Enable versioning
        )
        
    def _is_valid_bucket_name(self, name: str) -> bool:
        """Validate bucket name against AWS naming rules."""
        if not isinstance(name, str):
            return False
        # AWS bucket naming rules
        return bool(re.match(r'^[a-z0-9][a-z0-9.-]{1,61}[a-z0-9]$', name)) and \
               not name.startswith('aws-') and \
               not name.endswith('-bucket') and \
               not name.endswith('-s3') and \
               not name.startswith('s3-')

# Usage example
# app = core.App()
# secure_bucket = SecureS3Bucket(app, "my-secure-bucket", "my-secure-bucket-name")
# app.synth()
```