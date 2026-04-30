import os
import re
from typing import Optional
import aws_cdk as cdk
from aws_cdk import aws_s3 as s3

class SecureS3BucketStack(cdk.Stack):
    def __init__(self, scope: cdk.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)
        
        # Validate bucket name
        if not self._is_valid_bucket_name(bucket_name):
            raise ValueError("Invalid bucket name format")
            
        # Create S3 bucket with secure defaults
        self.bucket = s3.Bucket(
            self, 
            bucket_name=bucket_name,
            versioned=True,  # Enable versioning
            encryption=s3.BucketEncryption.S3_MANAGED_KEY_ALGORITHM_256,  # Use 256-bit AES encryption
            block_public_acls=True,  # Block public ACLs
            block_public_policy=True,  # Block public policies
            object_encryption=s3.BucketObjectEncryption.S3_MANAGED_KEY_ALGORITHM_256,  # Encrypt objects
            # Add more security settings as needed
        )

    @staticmethod
    def _is_valid_bucket_name(name: str) -> bool:
        """Validate bucket name format and restrictions"""
        # Bucket names must be 3-63 chars long, can only contain lowercase letters, numbers, dots, and hyphens
        pattern = r'^[a-z0-9][a-z0-9.-]{1,61}[a-z0-9]$'
        return bool(re.match(pattern, name))

def main():
    app = cdk.App()
    # Get bucket name from environment variable
    bucket_name = os.environ.get('S3_BUCKET_NAME')
    if not bucket_name:
        raise ValueError("S3_BUCKET_NAME environment variable not set")
    
    # Create stack
    SecureS3BucketStack(app, "secure-s3-bucket", bucket_name=bucket_name)

if __name__ == "__main__":
    main()