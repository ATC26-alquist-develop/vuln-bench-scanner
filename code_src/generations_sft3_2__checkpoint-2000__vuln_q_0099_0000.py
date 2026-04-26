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
            bucket_name=f"secure-bucket-{cdk.Aws.RandomValueGenerator.generate().string(8)}",
            versioned=True,
            encryption=s3.BucketEncryption.KMS_MANAGED,
            removal_policy=cdk.RemovalPolicy.DESTROY,  # Secure: delete on stack removal
            auto_delete_objects=True,
            public_read_access=False,
            block_public_access=s3.BlockPublicAccess.BLOCK_ALL
        )

        # Add any additional customizations here