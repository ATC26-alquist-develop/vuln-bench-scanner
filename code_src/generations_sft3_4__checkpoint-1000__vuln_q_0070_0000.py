from aws_cdk import core
from aws_cdk.aws_s3 import Bucket
from aws_cdk.aws_s3_deployment import (
    BucketDeployment,
    Source
)
from constructs import Construct

class SecureS3BucketStack(core.Stack):

    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Create a secure bucket with default policies
        bucket = Bucket(
            self,
            "SecureBucket",
            versioned=False,  # Disable versioning for security
            encryption=BucketEncryption.KMS_MANAGED,  # Use server-side encryption
            removal_policy=core.RemovalPolicy.DESTROY,  # Secure deletion
            auto_delete_objects=True,  # Enable auto-deletion
            block_public_access=BucketBlockPublicAccess.BLOCK_ALL,  # Prevent public access
            public_read_access=False,  # Disable public read access
            auto_delete_objects_versioned=True  # Enable auto-deletion for versions
        )

        # Deploy static content (example)
        bucket.add_public_access_block()
        bucket.grant_read(core.CfnOutput(self, "BucketUrl", value=bucket.bucket_url))

        # Add any additional security configurations here