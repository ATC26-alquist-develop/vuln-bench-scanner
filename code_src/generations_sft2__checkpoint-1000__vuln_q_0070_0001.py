import os
import logging
from typing import Optional
from aws_cdk import core
from aws_cdk import aws_s3 as s3

class SecureS3Bucket(core.Construct):
    def __init__(self, scope: core.Construct, id: str, bucket_name: str, **kwargs):
        super().__init__(scope, id)
        self.bucket_name = bucket_name
        self._setup_logging()
        self._create_bucket()

    def _setup_logging(self):
        """Set up logging for debugging and auditing"""
        logging.basicConfig(level=logging.INFO)
        logger = logging.getLogger(__name__)
        logger.info(f"Creating bucket: {self.bucket_name}")

    def _create_bucket(self):
        """Create S3 bucket with security best practices"""
        try:
            # Create bucket with default encryption
            bucket = s3.Bucket(self, 
                              self.bucket_name,
                              encryption=s3.BucketEncryption.S3_MANAGED,
                              block_public_acls=True,
                              generate_public_url=False,
                              removal_policy=core.RemovalPolicy.DESTROY)
            
            # Enable versioning
            bucket.versioning().enabled(True)
            
            # Set up logging
            bucket.add_tags(
                tags=[
                    core.Tag(key="Name", value=self.bucket_name),
                    core.Tag(key="Environment", value="Production")
                ]
            )
            
            logger.info(f"Successfully created bucket: {self.bucket_name}")
        except Exception as e:
            logger.error(f"Failed to create bucket: {str(e)}")
            raise

def main():
    app = core.App()
    bucket_name = os.environ.get('S3_BUCKET_NAME')
    if not bucket_name:
        raise ValueError("S3_BUCKET_NAME environment variable not set")
    
    SecureS3Bucket(app, "secure-s3-bucket", bucket_name)

if __name__ == "__main__":
    main()