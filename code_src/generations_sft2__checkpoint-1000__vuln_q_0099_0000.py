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
        
        # Get credentials from environment variables
        aws_access_key_id = os.environ.get('AWS_ACCESS_KEY_ID')
        aws_secret_access_key = os.environ.get('AWS_SECRET_ACCESS_KEY')
        aws_region = os.environ.get('AWS_REGION')
        
        # Validate credentials
        if not all([aws_access_key_id, aws_secret_access_key, aws_region]):
            logger.error("Missing required AWS credentials in environment variables")
            raise ValueError("AWS credentials not found in environment variables")
            
        # Validate bucket name
        if not isinstance(bucket_name, str) or not bucket_name:
            logger.error("Invalid bucket name")
            raise ValueError("Bucket name must be a non-empty string")
            
        # Create bucket with secure defaults
        bucket = s3.Bucket(
            self, 
            bucket_name=bucket_name,
            removal_policy=core.RemovalPolicy.DESTROY,  # Use with caution
            block_public_access=s3.BlockPublicAccess.BLOCK_ALL,  # Block all public access
            encryption=s3.BucketEncryption.S3_MANAGED,  # Enable default encryption
            versioning=s3.BucketVersioning.ENABLED,  # Enable versioning
            tags=[core.Tag(key="Name", value=bucket_name)]
        )
        
        logger.info(f"Created bucket: {bucket.bucket_name}")