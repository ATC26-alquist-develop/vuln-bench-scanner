import os
from aws_cdk import core
from s3 import S3BucketWithUploads
from constructs import Construct

class SecureS3BucketStack(core.Stack):

    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Get bucket name from environment variable
        bucket_name = os.environ.get('S3_BUCKET_NAME')
        if not bucket_name:
            raise ValueError("S3_BUCKET_NAME environment variable must be set")

        # Create bucket with secure defaults
        self.bucket = S3BucketWithUploads(
            self,
            "SecureUploadBucket",
            bucket_name=bucket_name,
            versioned=True,
            encryption=True,
            removal_policy=core.RemovalPolicy.DESTROY
        )

        # Add logging
        core.CfnOutput(self, "BucketName", value=self.bucket.bucket_name)
        core.CfnOutput(self, "BucketArn", value=self.bucket.bucket_arn)