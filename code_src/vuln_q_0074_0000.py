import os
import logging
from aws_cdk import core, aws_s3 as s3
from aws_cdk.exceptions import InvalidParameter, CfnResourceNotFound
from typing import Optional

class SecureS3Bucket(core.Construct):
    def __init__(self, scope: core.Construct, id: str, bucket_name: str, encryption_key: Optional[str] = None, **kwargs):
        super().__init__(scope, id)
        
        # Validate bucket name
        if not self._is_valid_bucket_name(bucket_name):
            raise InvalidParameter("Invalid bucket name")
            
        # Use default encryption
        encryption = s3.BucketEncryption(
            rules=[
                s3.BucketEncryptionRule(
                    server_side_encryption_configuration={
                        'rules': [{
                            'apply_server_side_encryption_by_default': {
                                'sse_algorithm': 'AES256'
                            }
                        }]
                    }
                )
            ]
        )
        
        # Create bucket with encryption
        self.bucket = s3.Bucket(
            self, 
            bucket_name=bucket_name,
            encryption=encryption,
            **kwargs
        )
        
        # Set default bucket policy
        self._set_bucket_policy(bucket_name)

    def _is_valid_bucket_name(self, name: str) -> bool:
        """Validate bucket name against AWS naming rules."""
        return (len(name) <= 63 and
                name.islower() and
                name.replace('-', '').isalnum() and
                not name.startswith('aws-') and
                not name.endswith('-aws'))

    def _set_bucket_policy(self, bucket_name: str) -> None:
        """Set secure default bucket policy."""
        policy = {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Sid": "DenyAllRequests",
                    "Effect": "Deny",
                    "Principal": "*",
                    "Action": "*",
                    "Resource": f"arn:aws:s3:::{bucket_name}/*",
                    "Condition": {
                        "StringNotEquals": {
                            "aws:SourceArn": "arn:aws:iam::123456789012:root"  # Replace with your account ID
                        }
                    }
                }
            ]
        }
        self.bucket.add_to_resource_policy(policy)

# Usage example
class MyStack(core.Stack):
    def __init__(self, scope: core.Construct, id: str, bucket_name: str, encryption_key: Optional[str] = None, **kwargs):
        super().__init__(scope, id)
        bucket = SecureS3Bucket(self, f"MySecureBucket-{id}", bucket_name, encryption_key=encryption_key)