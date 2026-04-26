from aws_cdk import core as cdk
from aws_cdk import aws_s3 as s3
from constructs import Construct

class SecureS3BucketStack(cdk.Stack):

    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Create a secure bucket with default policies
        self.bucket = s3.Bucket(
            self,
            "SecureBucket",
            bucket_name=f"secure-bucket-{cdk.ArnGenerator.generate_id_for_terminals()}",
            versioned=True,
            encryption=s3.BucketEncryption.S3_MANAGED,
            removal_policy=cdk.RemovalPolicy.DESTROY,  # Secure: auto-deletes on stack update
            auto_delete_objects=True,
            public_access_block_configuration={
                "block_public_access": s3.PublicAccess.BLOCK_ALL
            }
        )

        # Add any additional secure configurations here