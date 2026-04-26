from aws_cdk import core as cdk
from aws_cdk import aws_s3 as s3
from constructs import Construct

class SimpleS3BucketStack(cdk.Stack):

    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Create a bucket with secure defaults
        self.bucket = s3.Bucket(
            self,
            "SecureBucket",
            bucket_name=f"myapp-{cdk.Aws.REGION}-{cdk.Aws.CLOUDFORMATION_STACK_NAME}",
            versioned=True,
            encryption=s3.BucketEncryption.KMS,
            removal_policy=cdk.RemovalPolicy.DESTROY,  # Secure: auto-deletes on stack update
            auto_delete_objects=True,
            public_read_access=False,
            block_public_access=s3.BlockPublicAccess.BLOCK_ALL
        )