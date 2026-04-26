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

        # Create a secure S3 bucket with proper defaults
        bucket = Bucket(
            self,
            "SecureBucket",
            bucket_name=f"secure-bucket-{self.region}-{self.account}",
            removal_policy=core.RemovalPolicy.DESTROY,  # Secure: Remove on stack update
            versioned=False,  # Disable versioning for security
            encryption=BucketEncryption.KMS_MANAGED,  # Use KMS for encryption
            block_public_access=BucketBlockPublicAccess.BLOCK_ALL,  # Prevent public access
            auto_delete_objects=True,  # Enable auto-deletion
            public_read_access=False,  # Disable public read access
            auto_delete_objects_versioned=True  # Enable version auto-deletion
        )

        # Secure deployment of content
        source = Source.local(
            path="./content"
        )
        
        # Deploy content to bucket with proper validation
        BucketDeployment(
            self,
            "DeployContent",
            sources=[source],
            destination_bucket=bucket,
            destination_key_prefix="content/"
        )

        # Add logging for security events
        core.CfnOutput(
            self,
            "BucketARN",
            value=bucket.bucket_arn,
            export_name=f"{self.stack_name}-BucketARN"
        )