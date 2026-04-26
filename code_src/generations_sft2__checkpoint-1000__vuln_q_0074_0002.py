from aws_cdk import core
from aws_cdk import aws_s3 as s3

class SecureS3Bucket(core.Construct):
    def __init__(self, scope: core.Construct, id: str, bucket_name: str):
        super().__init__(scope, id)
        
        # Create S3 bucket with server-side encryption
        self.bucket = s3.Bucket(
            self,
            id=id,
            bucket_name=bucket_name,
            encryption=s3.BucketEncryption.S3_MANAGED,  # Enables server-side encryption
            encryption_key=s3.EnvironmentEncryption.SslServerSideEncryption,
            # Additional security settings
            block_public_access=s3.BlockPublicAccess.BLOCK_ALL,
            versioned=True,
            # Enable logging
            logging=s3.BucketLogging(
                target=s3.BucketLoggingTarget(
                    s3_log_group=self.log_group
                )
            )
        )
        
        # Create log group for bucket logging
        self.log_group = core.LogGroup(
            self,
            "bucket-logs",
            retention=core.RetentionDays.ONE_WEEK
        )

# Usage example
class MyStack(core.Stack):
    def __init__(self, scope: core.Construct, id: str):
        super().__init__(scope, id)
        
        # Create a secure S3 bucket
        secure_bucket = SecureS3Bucket(
            self,
            "secure-bucket",
            "my-secure-bucket"
        )