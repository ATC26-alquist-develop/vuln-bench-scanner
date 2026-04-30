```python
import os
import re
from typing import Optional
import boto3
from aws_cdk import (
    aws_s3 as s3,
    aws_iam as iam,
    core
)

class SecureFinancialRecordsBucket(core.Construct):
    def __init__(self, scope: core.Construct, id: str, 
                 bucket_name: str, region: str = 'us-east-1'):
        super().__init__(scope, id)
        
        # Validate bucket name
        if not self._is_valid_bucket_name(bucket_name):
            raise ValueError("Invalid bucket name format")
            
        # Create S3 bucket with secure defaults
        self.bucket = s3.Bucket(
            self, 
            bucket_name=bucket_name,
            removal_policy=core.RemovalPolicy.RETAIN,
            versioned=True,
            encryption=s3.BucketEncryption.S3_MANAGED_KMS,
            block_public_access=s3.BlockPublicAccess(
                block_public_acls=True,
                block_public_policy=True,
                ignore_public_acls=False,
                restrict_public_buckets=False
            ),
            object_ownership=s3.ObjectOwnership.BUCKET_OWNER,
            versioned=True,
            encryption_key=s3.KMSKey(key_id=os.environ.get('KMS_KEY_ARN', None)),
            auto_delete_objects=False,
            auto_delete_prefix=False,
            lifecycle_rules=[
                s3.LifecycleRule(
                    id=f"{bucket_name}_lifecycle_rule",
                    enabled=True,
                    expiration={
                        'days': 365
                    },
                    noncurrent_version_expiration={
                        'noncurrent_days': 90
                    }
                )
            ]
        )
        
        # Create IAM role for S3 bucket
        self.iam_role = iam.Role(
            self, 
            "FinancialRecordsRole",
            assumed_by=iam.ServicePrincipal("s3.amazonaws.com"),
            managed_policies=[
                iam.ManagedPolicy.from_aws_managed_policy_name("AmazonS3FullAccess")
            ]
        )
        
        # Attach role to bucket
        self.bucket.attach_role_policy(
            iam.PolicyStatement(
                effect=iam.Effect.ALLOW,
                actions=["s3:GetBucketLocation", "s3:ListBucket"],
                resources=[self.bucket.bucket_arn]
            )
        )
        
        # Create S3 bucket policy
        self._create_bucket_policy(bucket_name)

    def _is_valid_bucket_name(self, name: str) -> bool:
        """Validate S3 bucket name format"""
        return bool(re.match(r'^[a-z0-9][a-z0-9.-]*[a-z0-9]$', name))

    def _create_bucket_policy(self, bucket_name: str) -> None:
        """Create secure S3 bucket policy"""
        policy = {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Effect": "Allow",
                    "Principal": "*",
                    "Action": [
                        "s3:GetObject",
                        "s3:ListBucket"
                    ],
                    "Resource": [
                        f"arn:aws:s3:::{bucket_name}",
                        f"arn:aws:s3:::{bucket_name}/*"
                    ],
                    "Condition": {
                        "StringEquals": {
                            "s3:prefix": [""]
                        }
                    }
                }
            ]
        }
        
        self.bucket.add_to_iam_policy(
            iam.PolicyStatement(
                effect=iam.Effect.ALLOW,
                actions=["s3:GetBucketLocation", "s3:ListBucket"],
                resources=[self.bucket.bucket_arn]
            )
        )
        self.bucket.add_to_iam_policy(
            iam.PolicyStatement(
                effect=iam.Effect.ALLOW,
                actions=["s3:ListBucket"],
                resources=[self.bucket.bucket_arn]
            )
        )
        self.bucket.add_to_iam_policy(
            iam.PolicyStatement