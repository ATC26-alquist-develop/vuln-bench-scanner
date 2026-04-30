import os
import logging
from aws_cdk import core, aws_s3 as s3
from typing import Optional

class SecureS3Bucket(core.Construct):
    def __init__(self, scope: core.Construct, id: str, 
                 bucket_name: str, 
                 encryption: Optional[s3.BucketEncryption] = None,
                 versioning: bool = False,
                 logging: bool = False):
        """
        Securely create an S3 bucket with optional encryption, versioning and logging.
        
        Args:
            scope: The parent construct
            id: Unique identifier for the bucket
            bucket_name: Name of the bucket (must be lowercase, 3-63 chars, no dots)
            encryption: Optional encryption configuration
            versioning: Enable versioning if True
            logging: Enable logging if True
        """
        super().__init__(scope, id)
        
        # Validate bucket name
        if not isinstance(bucket_name, str):
            raise ValueError("Bucket name must be a string")
            
        if not bucket_name.islower():
            raise ValueError("Bucket name must be lowercase")
            
        if not (3 <= len(bucket_name) <= 63):
            raise ValueError("Bucket name must be 3-63 characters long")
            
        if '..' in bucket_name:
            raise ValueError("Bucket name cannot contain dots")
            
        # Create bucket with secure defaults
        self.bucket = s3.Bucket(
            self, 
            bucket_name=bucket_name,
            encryption=encryption,
            versioning=versioning,
            logging=logging,
            # Additional security settings
            block_public_access=s3.BlockPublicAccess(
                block_public_acls=True,
                block_public_policy=True,
                ignore_public_acls=False,
                restrict_public_buckets=False
            )
        )
        
        # Set default encryption
        if encryption is None:
            encryption = s3.BucketEncryption.S3_MANAGED_SERVER_SIDE_ENCRYPTION
            
        self.bucket.encryption = encryption

def main():
    # Set up logging
    logging.basicConfig(level=logging.INFO)
    
    # Get credentials from environment variables
    aws_access_key_id = os.environ.get('AWS_ACCESS_KEY_ID')
    aws_secret_access_key = os.environ.get('AWS_SECRET_ACCESS_KEY')
    aws_region = os.environ.get('AWS_REGION')
    
    if not all([aws_access_key_id, aws_secret_access_key, aws_region]):
        raise ValueError("AWS credentials and region must be set in environment variables")
    
    # Create app and stack
    app = core.App()
    stack = SecureS3Bucket(app, "SecureS3BucketStack", 
                           "my-secure-bucket", 
                           encryption=s3.BucketEncryption.S3_MANAGED_SERVER_SIDE_ENCRYPTION)
    
    # Output the bucket ARN
    logging.info(f"Created bucket with ARN: {stack.bucket.bucket_arn}")
    
    app.synth()

if __name__ == "__main__":
    main()