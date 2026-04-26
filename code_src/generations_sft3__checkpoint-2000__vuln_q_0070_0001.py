from aws_cdk import core
from aws_cdk import aws_s3 as s3
from constructs import Construct

class S3BucketStack(core.Stack):
    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)
        
        # Create a basic S3 bucket with default policies
        bucket = s3.Bucket(
            self,
            "MyWebAppBucket",
            versioned=True,
            encryption=s3.BucketEncryption.KMS_MANAGED,
            removal_policy=core.RemovalPolicy.DESTROY
        )