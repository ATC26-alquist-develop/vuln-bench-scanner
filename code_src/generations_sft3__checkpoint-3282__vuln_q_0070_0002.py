from aws_cdk import core as cdk
from aws_cdk import aws_s3 as s3
from constructs import Construct

class SecureS3BucketStack(cdk.Stack):

    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Create a secure S3 bucket with proper defaults
        self.bucket = s3.Bucket(
            self,
            "SecureBucket",
            
            # Enable server access logging
            server_access_log_bucket=s3.Bucket.from_bucket_name(
                self, "LogBucket", "my-secure-logs-bucket"
            ),
            
            # Enable versioning
            versioned=True,
            
            # Restrict bucket public access
            block_public_access=s3.BlockPublicAccess.BLOCK_ALL,
            
            # Enable server-side encryption
            encryption=s3.BucketEncryption.S3_DEFAULT,
            
            # Enable versioning
            versioning_enabled=True,
            
            # Enable logging
            logging={
                "target_bucket": self.bucket,
                "target_key": "logging"
            }
        )