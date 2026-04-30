import os
import logging
from aws_cdk import core, aws_s3 as s3
from typing import Optional

class SecureS3Bucket(core.Construct):
    def __init__(self, scope: core.Construct, id: str, 
                 bucket_name: str, 
                 encryption: Optional[s3.BucketEncryption] = None,
                 versioning: bool = False,
                 public_access_block: bool = True,
                 tags: Optional[dict] = None):
        """
        Creates a secure S3 bucket with recommended security settings.
        
        Args:
            scope: The parent construct
            id: Unique identifier for the bucket
            bucket_name: Name of the bucket (must be lowercase, 3-63 chars)
            encryption: Optional encryption configuration
            versioning: Enable versioning if needed
            public_access_block: Block public access by default
            tags: Optional dictionary of tags
        """
        # Validate bucket name
        if not isinstance(bucket_name, str):
            raise ValueError("Bucket name must be a string")
        if not bucket_name.islower() or not 3 <= len(bucket_name) <= 63:
            raise ValueError("Invalid bucket name format")
            
        # Create bucket with secure defaults
        super().__init__(scope, id)
        
        # Create bucket with encryption
        self.bucket = s3.Bucket(
            self, 
            bucket_name=bucket_name,
            encryption=encryption,
            versioning=versioning,
            public_access_block=public_access_block,
            tags=tags
        )
        
        # Set default encryption
        if not encryption:
            self.bucket.encryption = s3.BucketEncryption.S3_MANAGED_SERVER_SIDE_ENCRYPTION
            
        # Log bucket creation
        logging.info(f"Created secure S3 bucket: {self.bucket.bucket_name}")

def main():
    app = core.App()
    try:
        bucket = SecureS3Bucket(
            scope=app,
            id="secure-bucket",
            bucket_name="my-secure-bucket",
            encryption=s3.BucketEncryption.S3_MANAGED_SERVER_SIDE_ENCRYPTION,
            versioning=True,
            public_access_block=True,
            tags={"Environment": "Production"}
        )
        app.synth()
    except Exception as e:
        logging.error(f"Failed to create S3 bucket: {str(e)}")
        raise

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()