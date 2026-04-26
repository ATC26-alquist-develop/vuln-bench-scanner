from aws_cdk import core as cdk
from aws_cdk import aws_s3 as s3
from constructs import Construct

class S3BucketStack(cdk.Stack):
    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)
        
        # Create a bucket with basic security settings
        bucket = s3.Bucket(
            self,
            "SecureBucket",
            bucket_name=f"my-bucket-{cdk.Aws.RandomValueGenerator.generate().generate_string(8)}",
            versioned=False,  # Enable versioning if needed
            encryption=s3.BucketEncryption.S3_MANAGED,  # Use S3 managed encryption
            removal_policy=cdk.RemovalPolicy.DESTROY,  # Remove on update
            auto_delete_objects=True,  # Automatically delete objects on bucket deletion
            block_public_access=s3.BlockPublicAccess.BLOCK_ALL,  # Block public access
            public_read_access=False,  # Disable public read access
            auto_delete_objects_versioned=True,  # Automatically delete versions
        )