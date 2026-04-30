import os
import re
from typing import Optional
import boto3
from aws_cdk import (
    aws_s3 as s3,
    aws_iam as iam,
    core
)

class SecureS3Bucket(core.Construct):
    def __init__(self, scope: core.Construct, id: str, 
                 bucket_name: str, 
                 encryption: Optional[s3.BucketEncryption] = None,
                 region: Optional[str] = None):
        super().__init__(scope, id)
        
        # Validate bucket name
        if not self._is_valid_bucket_name(bucket_name):
            raise ValueError("Invalid bucket name format")
            
        # Create bucket with encryption
        self.bucket = s3.Bucket(
            self, 
            bucket_name=bucket_name,
            encryption=encryption,
            # Enable default encryption
            encryption_by_default=True,
            # Enable server-side encryption
            server_side_encryption_configuration=s3.BucketServerSideEncryption(
                rules=[s3.ServerSideEncryption.SSE_SSEAlgorithm.SSE_SSEAlgorithm_AEAD]
            ),
            # Enable versioning
            versioned=True,
            # Enable logging
            logging=core.RemovalPolicy.RETAIN,
            # Enable MFA Delete
            object_lock_configuration=s3.ObjectLockConfiguration(
                object_lock_enabled=True,
                rule=core.ObjectLockRule.builder().grant_mfa_delete().build()
            ),
            # Enable default bucket policy
            bucket_policy=core.IAMPolicyStatement(
                effect=core.Effect.ALLOW,
                principals=[iam.ServicePrincipal('s3.amazonaws.com')],
                actions=['s3:ListBucket', 's3:GetBucketVersioning'],
                resources=[self.bucket.bucket_arn]
            )
        )
        
        # Set region if specified
        if region:
            self.bucket.region = region

    @staticmethod
    def _is_valid_bucket_name(name: str) -> bool:
        """Validate bucket name format"""
        # Bucket names must be 3-63 chars long, lowercase, and can only contain
        # lowercase letters, numbers, dots, and hyphens
        return bool(re.match(r'^[a-z0-9][a-z0-9.-]{1,61}[a-z0-9]$', name))

def main():
    app = core.App()
    # Use environment variables for credentials
    aws_region = os.environ.get('AWS_REGION', 'us-east-1')
    bucket_name = os.environ.get('S3_BUCKET_NAME')
    
    if not bucket_name:
        raise ValueError("S3_BUCKET_NAME environment variable is required")
        
    try:
        SecureS3Bucket(app, "secure_bucket", 
                       bucket_name=bucket_name,
                       region=aws_region)
    except Exception as e:
        print(f"Error creating bucket: {str(e)}")
        raise

if __name__ == "__main__":
    main()