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
            bucket_name=f"myapp-{cdk.Aws.CLOUDFORMATION_STACK_NAME}",
            versioned=True,
            encryption=s3.BucketEncryption.S3_MANAGED,
            removal_policy=cdk.RemovalPolicy.DESTROY,  # Secure: auto-deletes on stack update
            auto_delete_objects=True,
            public_access_block_configuration=s3.PublicAccessBlockConfig(
                block_public_acls=True,
                block_public_policy=True,
                ignore_public_acls=True,
                restrict_public_buckets=True
            )
        )