from aws_cdk import core as cdk
from aws_cdk import aws_s3 as s3
from constructs import Construct

class SimpleS3BucketStack(cdk.Stack):

    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Create a simple bucket with secure defaults
        bucket = s3.Bucket(
            self,
            "SecureBucket",
            bucket_name=f"myapp-{cdk.Aws.CLOUDFORMATIONSTACKSET_NAME or cdk.Aws.ACCOUNT_ID}",
            versioned=True,
            encryption=s3.BucketEncryption.S3_MANAGED,
            removal_policy=cdk.RemovalPolicy.DESTROY,  # Secure: delete on stack update
            auto_delete_objects=cdk.Duration.days(7),
            public_access_block_configuration=[
                s3.PublicAccessBlockConfigRule(block_public_acls=True),
                s3.PublicAccessBlockConfigRule(block_public_policy=True),
                s3.PublicAccessBlockConfigRule(restrict_public_buckets=True)
            ]
        )

        # Add any additional customizations here