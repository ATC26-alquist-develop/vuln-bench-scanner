import os
import logging
from typing import Optional
import boto3
from aws_cdk import aws_s3 as s3, aws_kms as kms
from aws_cdk.core import Stack, Duration, RetentionDays

class SecureKMSBucketStack(Stack):
    def __init__(self, scope: Stack, id: str, bucket_name: str, kms_key_id: Optional[str] = None, **kwargs):
        super().__init__(scope, id, **kwargs)
        
        # Configure logging
        logging.basicConfig(level=logging.INFO)
        logger = logging.getLogger(__name__)
        
        # Validate bucket name
        if not self._is_valid_bucket_name(bucket_name):
            raise ValueError("Invalid bucket name")
            
        # Create KMS key if not provided
        if not kms_key_id:
            kms_key = kms.Key(self, f"{bucket_name}-kms-key",
                              removal_policy=aws_cdk.RemovalPolicy.DESTROY,
                              description="KMS key for bucket encryption")
            kms_key_key_id = kms_key.key_id
        else:
            kms_key_key_id = kms_key_id
            
        # Create S3 bucket with encryption
        bucket = s3.Bucket(self, id=bucket_name,
                          encryption=s3.BucketEncryption.KMS,
                          encryption_kms_key=kms_key_key_id,
                          removal_policy=aws_cdk.RemovalPolicy.DESTROY,
                          block_public_access=s3.BlockPublicAccess.BLOCK_ALL,
                          lifecycle_rules=[s3.LifecycleRule(
                              id=f"{bucket_name}-lifecycle",
                              enabled=True,
                              expiration={
                                  'days': RetentionDays.ONE_WEEK
                              },
                              noncurrent_version_expiration={
                                  'noncurrent_days': RetentionDays.ONE_WEEK
                              }
                          )])
        
        logger.info(f"Created bucket {bucket_name} with encryption using KMS key {kms_key_key_id}")

    @staticmethod
    def _is_valid_bucket_name(bucket_name: str) -> bool:
        """Validate bucket name against AWS naming rules."""
        if not isinstance(bucket_name, str):
            return False
        if len(bucket_name) > 63:
            return False
        if not bucket_name.isalnum() and not bucket_name.replace('_', '').isalnum():
            return False
        return True