import os
import logging
from typing import Optional
import boto3
from aws_cdk import core
from aws_cdk import aws_s3 as s3
from aws_cdk import aws_kms as kms

class SecureS3Bucket(core.Construct):
    def __init__(self, scope: core.Construct, id: str, bucket_name: str, kms_key: Optional[kms.Key] = None):
        super().__init__(scope, id)
        self.bucket_name = bucket_name
        self.kms_key = kms_key
        self._setup_bucket()

    def _setup_bucket(self) -> None:
        """Set up S3 bucket with encryption and logging"""
        # Create S3 bucket with default encryption
        self.bucket = s3.Bucket(self, 
            bucket_name=self.bucket_name,
            encryption=s3.BucketEncryption.S3_MANAGED,
            removal_policy=s3.RemovalPolicy.DESTROY,
            logging=core.LoggingBucket(self, 
                bucket_name=f"{self.bucket_name}-logs",
                encryption=s3.BucketEncryption.S3_MANAGED
            )
        )
        
        # Enable server-side encryption
        self.bucket.encryption = s3.BucketEncryption.S3_MANAGED
        
        # Set up KMS key if provided
        if self.kms_key:
            self.bucket.encryption.key = self.kms_key

    def get_bucket_name(self) -> str:
        """Return the bucket name"""
        return self.bucket_name

class SecureS3BucketStack(core.Stack):
    def __init__(self, scope: core.Construct, id: str, bucket_name: str, kms_key_arn: Optional[str] = None):
        super().__init__(scope, id)
        
        # Validate inputs
        if not isinstance(bucket_name, str) or not bucket_name:
            raise ValueError("Invalid bucket name")
            
        if kms_key_arn and not isinstance(kms_key_arn, str):
            raise ValueError("Invalid KMS key ARN")
            
        # Create KMS key if not provided
        kms_key = None
        if not kms_key_arn:
            kms_key = kms.Key(self, 
                "KMSKey",
                alias_name="alias/sensitive-data",
                description="KMS key for encrypting sensitive data"
            )
            
        # Create secure S3 bucket
        secure_bucket = SecureS3Bucket(self, 
            id=f"secure-{bucket_name}",
            bucket_name=bucket_name,
            kms_key=kms_key
        )

    def get_bucket_name(self) -> str:
        """Return the bucket name"""
        return secure_bucket.get_bucket_name()