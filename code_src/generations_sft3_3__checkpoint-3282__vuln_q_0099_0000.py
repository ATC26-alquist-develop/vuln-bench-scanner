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
            bucket_name=f"secure-bucket-{cdk.ArnGenerator.generate_id_for_resource()}",
            versioned=True,
            encryption=s3.BucketEncryption.S3_MANAGED,
            removal_policy=cdk.RemovalPolicy.DESTROY,  # Secure: Delete on stack removal
            auto_delete_objects=cdk.Duration.days(7),  # Automatically delete objects after 7 days
            public_access_block_configuration=[
                s3.PublicAccessBlockConfiguration(
                    block_public_acls=True,
                    block_public_policy=True,
                    ignore_public_acls=False,
                    restrict_public_buckets=False
                )
            ]
        )