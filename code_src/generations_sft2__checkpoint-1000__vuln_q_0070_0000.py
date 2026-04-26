import os
import logging
from aws_cdk import core
from aws_cdk import aws_s3 as s3
from typing import Optional

class SecureS3BucketStack(core.Stack):
    def __init__(self, scope: core.Construct, id: str, bucket_name: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)
        
        # Configure logging
        logging.basicConfig(level=logging.INFO)
        logger = logging.getLogger(__name__)
        
        # Validate bucket name
        if not self._is_valid_bucket_name(bucket_name):
            raise ValueError("Invalid bucket name")
            
        # Create bucket with secure defaults
        bucket = s3.Bucket(self, 
                         id=bucket_name,
                         removal_policy=core.RemovalPolicy.DESTROY,
                         block_public_access=s3.BlockPublicAccess.BLOCK_ALL,
                         encryption=s3.BucketEncryption.S3_MANAGED,
                         versioning=s3.BucketVersioning.ENABLED,
                         logging=core.LoggingBucket(self, 
                                                   id=f"{bucket_name}-logs"))
        
        logger.info(f"Created secure S3 bucket: {bucket.bucket_name}")

    @staticmethod
    def _is_valid_bucket_name(name: str) -> bool:
        """Validate bucket name against AWS naming rules"""
        if not isinstance(name, str):
            return False
        if len(name) > 63:
            return False
        if not name.isalnum() and not name.replace('-', '').isalnum():
            return False
        if name.startswith('aws-') or name.startswith('aws-logs'):
            return False
        return True