import os
import logging
from aws_cdk import core, aws_s3 as s3
from typing import Optional

class SecureS3Bucket(core.Construct):
    def __init__(self, scope: core.Construct, id: str, 
                 bucket_name: str, 
                 encryption: Optional[s3.BucketEncryption] = None,
                 versioning: bool = False,
                 block_public_access: bool = True,
                 tags: Optional[dict] = None):
        super().__init__(scope, id)
        
        # Validate bucket name
        if not isinstance(bucket_name, str) or not bucket_name:
            raise ValueError("Invalid bucket name")
            
        # Prevent bucket name collisions
        if s3.Bucket(bucket_name).bucket_name in s3.Bucket().bucket_name:
            raise ValueError("Bucket name already exists")
            
        # Configure bucket with security best practices
        self.bucket = s3.Bucket(
            self, 
            bucket_name=bucket_name,
            encryption=encryption,
            versioning=versioning,
            block_public_access=block_public_access,
            tags=tags
        )
        
        # Enable default encryption
        if not encryption:
            self.bucket.encryption=s3.BucketEncryption.S3_MANAGED_SERVER_SIDE_ENCRYPTION
            
        # Log bucket creation
        logging.info(f"Created secure S3 bucket: {bucket_name}")

def main():
    app = core.App()
    try:
        bucket = SecureS3Bucket(
            app, 
            "secure-bucket",
            "my-secure-bucket",
            encryption=s3.BucketEncryption.SSE_KMS,
            versioning=True,
            block_public_access=True,
            tags={"Owner": "MyCompany", "Project": "SecureData"}
        )
        app.synth()
    except Exception as e:
        logging.error(f"Failed to create S3 bucket: {str(e)}")
        raise

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()