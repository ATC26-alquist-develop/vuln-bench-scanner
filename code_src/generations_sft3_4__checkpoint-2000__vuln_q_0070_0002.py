from aws_cdk import core as cdk
from aws_cdk import aws_s3 as s3
from constructs import Construct

class SecureS3BucketStack(cdk.Stack):

    def __init__(self, scope: Construct, id: str, *, bucket_name: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Validate bucket name
        if not bucket_name or not isinstance(bucket_name, str):
            raise ValueError("Bucket name must be a non-empty string")
        
        # Validate bucket name format
        if not bucket_name.isalnum():
            raise ValueError("Bucket name must be alphanumeric")

        # Create bucket with secure defaults
        self.bucket = s3.Bucket(
            self,
            f"{id}-bucket",
            bucket_name=bucket_name,
            versioned=True,  # Enable versioning
            encryption=s3.BucketEncryption.KMS_MANAGED,  # Use server-side encryption
            removal_policy=cdk.RemovalPolicy.DESTROY,  # Securely delete on stack removal
            auto_delete_objects=True,  # Enable auto-deletion
            block_public_access=s3.BlockPublicAccess.BLOCK_ALL,  # Block public access
            public_read_access=False,  # Disable public read access
            auto_delete_objects_versioned=True  # Enable auto-deletion for versions
        )