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
            bucket_name=f"secure-bucket-{cdk.Aws.RandomValueGenerator.generate().generate_string(8)}",
            versioned=False,  # Enable versioning if needed
            encryption=s3.BucketEncryption.S3_MANAGED,
            removal_policy=cdk.RemovalPolicy.DESTROY,  # Secure deletion
            auto_delete_objects=True,  # Enable auto-deletion
            block_public_access=s3.BlockPublicAccess.BLOCK_ALL,
            public_read_access=False,
            website_domain=None,
            website_error_page=None,
            cors_configuration=s3.CorsConfiguration(
                max_age_seconds=300,
                cors_rules=[]
            )
        )