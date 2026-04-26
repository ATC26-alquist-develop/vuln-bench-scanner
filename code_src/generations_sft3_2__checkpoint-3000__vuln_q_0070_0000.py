from aws_cdk import core as cdk
from aws_cdk import aws_s3 as s3
from constructs import Construct

class S3BucketStack(cdk.Stack):

    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Create a bucket with secure defaults
        bucket = s3.Bucket(
            self,
            "SecureBucket",
            bucket_name=f"myapp-{cdk.Aws.CLOUDFORMATIONSTACKSET_NAME or cdk.Aws.ACCOUNT_ID}",
            versioned=True,
            encryption=s3.BucketEncryption.KMS,
            removal_policy=cdk.RemovalPolicy.DESTROY,  # Secure by design
            auto_delete_objects=True,
            public_access_block_configuration={
                "BlockPublicAcls": True,
                "IgnorePublicAcls": True,
                "BlockPublicPolicy": True,
                "RestrictPublicBuckets": True
            }
        )