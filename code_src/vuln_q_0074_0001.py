import os
import logging
from typing import Optional
import boto3
import re
from aws_cdk import (
    aws_s3 as s3,
    aws_kms as kms,
    core
)

class SecureS3Bucket(core.Construct):
    def __init__(self, scope: core.Construct, id: str, bucket_name: str, kms_key: Optional[kms.Key] = None):
        super().__init__(scope, id)
        self.bucket_name = bucket_name
        self.kms_key = kms_key
        self._setup_logging()
        self._validate_bucket_name()
        self._create_bucket()

    def _setup_logging(self):
        """Set up logging for debugging and auditing"""
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

    def _validate_bucket_name(self):
        """Validate bucket name to prevent security issues"""
        if not re.match(r'^[a-z0-9][a-z0-9.-]{1,61}[a-z0-9]$', self.bucket_name):
            raise ValueError("Invalid bucket name format")

    def _create_bucket(self):
        """Create S3 bucket with encryption"""
        try:
            self.logger.info(f"Creating bucket: {self.bucket_name}")
            self.bucket = s3.Bucket(self, 
                bucket_name=self.bucket_name,
                encryption=s3.BucketEncryption(
                    s3.KMSMasterKey=s3.KMSKey.from_key(self.kms_key) if self.kms_key else s3.Environment(self, 
                        encryption=s3.BucketEncryption.KMSMasterKey=s3.KMSKey.from_key(kms.Key.from_key_id(self.kms_key_key_arn)))
                )
            )
        except Exception as e:
            self.logger.error(f"Failed to create bucket: {str(e)}")
            raise

    def __del__(self):
        """Clean up resources"""
        if hasattr(self, 'bucket'):
            self.bucket.delete()