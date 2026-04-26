import os
import logging
from aws_cdk import core
from aws_cdk import aws_s3 as s3
from typing import Optional

class SecureS3BucketStack(core.Stack):
    def __init__(self, scope: core.Construct, id: str, bucket_name: Optional[str] = None, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)
        
        # Configure logging
        logging.basicConfig(level=logging.INFO)
        logger = logging.getLogger(__name__)
        
        # Get bucket name from environment variable or use default
        bucket_name = bucket_name or os.environ.get('S3_BUCKET_NAME')
        if not bucket_name:
            raise ValueError("S3 bucket name must be provided via environment variable or parameter")
            
        # Validate bucket name
        if not isinstance(bucket_name, str) or not bucket_name.strip():
            raise ValueError("Invalid bucket name")
            
        # Create bucket with secure defaults
        bucket = s3.Bucket(self, 
                         id=bucket_name,
                         removal_policy=core.RemovalPolicy.DESTROY,  # Use with caution
                         block_public_access=s3.BlockPublicAccess.BLOCK_ALL,
                         versioning=s3.BucketVersioning.ENABLED,
                         encryption=s3.BucketEncryption.S3_MANAGED,
                         logging=core.LoggingBucket(self, 
                                                   id=f"{bucket_name}-logs",
                                                   removal_policy=core.RemovalPolicy.DESTROY),
                         )
        
        logger.info(f"Created secure S3 bucket: {bucket.bucket_name}")