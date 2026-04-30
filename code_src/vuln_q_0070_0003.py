import os
import re
import boto3
import logging
from botocore.exceptions import ClientError
from aws_cdk import core, aws_s3 as s3

class SecureS3BucketStack(core.Stack):
    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)
        
        # Get bucket name from environment variable
        bucket_name = os.environ.get('S3_BUCKET_NAME')
        if not bucket_name:
            raise ValueError("S3_BUCKET_NAME environment variable is not set")
            
        # Validate bucket name
        if not re.match(r'^[a-z0-9][a-z0-9.-]{1,61}[a-z0-9]$', bucket_name):
            raise ValueError("Invalid bucket name format")
            
        # Create bucket with secure settings
        try:
            bucket = s3.Bucket(self, 
                              'SecureUploadBucket', 
                              bucket_name=bucket_name,
                              removal_policy=core.RemovalPolicy.DESTROY,
                              block_public_access=s3.BlockPublicAccess.BucketBlockPublicAccessConfig(
                                  block_public_acls=True,
                                  ignore_public_acls=False,
                                  block_public_policy=True,
                                  restrict_public_buckets=False
                              ),
                              object_encryption_enabled=True,
                              versioning=True,
                              logging=core.LoggingTarget(bucket_name, bucket_name)
                              )
        except ClientError as e:
            logging.error(f"Failed to create bucket: {e}")
            raise

# Usage example
# app = core.App()
# SecureS3BucketStack(app, "SecureUploadBucketStack", env=os.environ)
# app.synth()