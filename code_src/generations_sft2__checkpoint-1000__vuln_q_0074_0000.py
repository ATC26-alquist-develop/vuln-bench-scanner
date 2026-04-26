import os
import logging
from aws_cdk import core
from aws_cdk import aws_s3 as s3
from aws_cdk import aws_iam as iam
from aws_cdk import aws_kms as kms

class SecureS3BucketStack(core.Stack):
    def __init__(self, scope: core.Construct, id: str, bucket_name: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)
        
        # Configure logging
        logging.basicConfig(level=logging.INFO)
        logger = logging.getLogger(__name__)
        
        # Validate bucket name
        if not self._is_valid_bucket_name(bucket_name):
            raise ValueError("Invalid bucket name")
            
        # Create KMS key
        key_arn = kms.Key(self, "S3Key", 
                         alias=f"alias/{bucket_name}",
                         description=f"KMS key for {bucket_name} bucket")
        
        # Create S3 bucket with encryption
        bucket = s3.Bucket(self, 
                          id=f"{bucket_name}-bucket",
                          bucket_name=bucket_name,
                          encryption=s3.BucketEncryption.AWS_KMS_MANAGED,
                          encryption_key=key_arn,
                          block_public_access=s3.BlockPublicAccess.BLOCK_ALL,
                          versioning=s3.BucketVersioning.ACTIVE,
                          logging=core.LogBucket(f"{bucket_name}.log"),
                          removal_policy=core.RemovalPolicy.DESTROY)
        
        logger.info(f"Created secure S3 bucket: {bucket.bucket_name}")

    @staticmethod
    def _is_valid_bucket_name(name: str) -> bool:
        """Validate S3 bucket name according to AWS rules"""
        if not isinstance(name, str):
            return False
        if len(name) > 63:
            return False
        if not name.isalnum() and not name.replace('_', '').isalnum():
            return False
        if name.startswith('aws-') or name.endswith('-aws'):
            return False
        return True