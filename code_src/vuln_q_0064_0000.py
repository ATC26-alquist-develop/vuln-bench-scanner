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
            raise ValueError("Missing AWS credentials in environment variables")
            
        # Create S3 bucket with secure defaults
        self.bucket = s3.Bucket(
            self, 
            bucket_name=bucket_name,
            acl='private',  # Default to private access
            versioning=True,  # Enable versioning
            encryption=s3.BucketEncryption.S3_MANAGED,  # Enable default encryption
            block_public_acls=True,  # Block public ACLs
            block_public_policy=True,  # Block public policies
            object_lock_enabled=True,  # Enable object locking
            object_lock_retention_period=365  # Set retention period
        )
        
    def _is_valid_bucket_name(self, name: str) -> bool:
        """Validate bucket name against AWS naming rules."""
        if not isinstance(name, str):
            return False
        if len(name) > 63:
            return False
        if not name:
            return False
        if re.match(r'^[a-z0-9][a-z0-9.-]{1,61}[a-z0-9]$', name) is None:
            return False
        return True

# Usage example:
# app = core.App()
# secure_bucket = SecureS3Bucket(app, "my-secure-bucket", "my-secure-bucket-name")
# app.synth()