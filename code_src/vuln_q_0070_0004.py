import os
import re
from aws_cdk import core
from aws_cdk import aws_s3 as s3

class SecureS3BucketStack(core.Stack):
    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)
        
        # Get bucket name from environment variable with validation
        bucket_name = os.environ.get('S3_BUCKET_NAME')
        if not bucket_name or not re.match(r'^[a-zA-Z0-9][a-zA-Z0-9.-]{1,61}[a-zA-Z0-9]$', bucket_name):
            raise ValueError("Invalid bucket name format")
            
        # Create S3 bucket with default security settings
        self.bucket = s3.Bucket(self, 
            'SecureBucket', 
            bucket_name=bucket_name,
            removal_policy=core.RemovalPolicy.DESTROY,  # Use with caution in production
            block_public_access=s3.BlockPublicAccess.BLOCK_ALL
        )