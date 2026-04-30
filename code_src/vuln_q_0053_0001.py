```python
import os
import re
import boto3
from aws_cdk import core, aws_s3 as s3
from aws_cdk.core import Duration
from aws_cdk.core import SecretValue
from aws_cdk.core import RemovalPolicy
from aws_cdk.core import Tags
import logging

class SecureFinancialRecordsBucket(core.Construct):
    def __init__(self, scope: core.Construct, id: str, bucket_name: str, region: str):
        super().__init__(scope, id)
        
        # Validate bucket name
        if not self._is_valid_bucket_name(bucket_name):
            raise ValueError("Invalid bucket name")
            
        # Create S3 bucket with secure settings
        self.bucket = s3.Bucket(
            self, 
            bucket_name=bucket_name,
            removal_policy=RemovalPolicy.DESTROY,
            location_constraint=region,
            versioning_configuration=s3.BucketVersioningConfiguration(enabled=True),
            block_public_access=s3.BlockPublicAccess.BucketBlockPublicAccessConfiguration(
                block_public_acls=True,
                block_public_policy=True,
                ignore_public_acls=False,
                restrict_public_buckets=False
            ),
            encryption=s3.BucketEncryption.S3_MANAGED,
            logging_configuration={
                'target_prefix': 'logs/',
                'role_arn': self._get_logging_role_arn()
            },
            tags=[
                Tags.of(self, 'Name', 'FinancialRecordsBucket'),
                Tags.of(self, 'Environment', 'Production')
            ]
        )
        
    def _is_valid_bucket_name(self, name: str) -> bool:
        """Validate bucket name against AWS naming rules."""
        return bool(re.match(r'^[a-z0-9][a-z0-9.-]{1,61}[a-z0-9]$', name)) and not name.startswith('aws-')
        
    def _get_logging_role_arn(self) -> str:
        """Get ARN for logging role with minimal permissions."""
        return SecretValue.secrets_manager('LoggingRoleArn', 'arn:aws:iam::123456789012:role/LoggingRole')

# Usage example
class FinancialRecordsStack(core.Stack):
    def __init__(self, scope: core.Construct, id: str, bucket_name: str, region: str):
        super().__init__(scope, id)
        self.bucket = SecureFinancialRecordsBucket(self, f"SecureFinancialRecordsBucket-{id}", bucket_name, region)
```