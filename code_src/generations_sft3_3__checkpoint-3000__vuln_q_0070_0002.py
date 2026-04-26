from aws_cdk import core as cdk
from aws_cdk import aws_s3 as s3
from constructs import Construct

class SecureS3BucketStack(cdk.Stack):

    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Create a secure S3 bucket with default policies
        bucket = s3.Bucket(
            self,
            "SecureBucket",
            bucket_name=f"secure-bucket-{cdk.ArnGenerator.generate_hash()}",
            versioned=True,
            encryption=s3.BucketEncryption.KMS,
            removal_policy=cdk.RemovalPolicy.DESTROY,  # Secure: Remove on update
            auto_delete_objects=True,  # Secure: Automatically delete objects
            block_public_access=s3.BlockPublicAccess.BLOCK_ALL,
            public_read_access=False,
            website_index_document="index.html",
            website_error_document="error.html"
        )

        # Add any additional secure configurations here