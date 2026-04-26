from aws_cdk import core as cdk
from aws_cdk import aws_s3 as s3
from constructs import Construct

class SecureS3BucketStack(cdk.Stack):

    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Create a secure S3 bucket with proper defaults
        self.bucket = s3.Bucket(
            self,
            "SecureBucket",
            bucket_name=f"secure-bucket-{cdk.ArnGenerator.generate_hash()}",
            versioned=True,
            encryption=s3.BucketEncryption.KMS,
            removal_policy=cdk.RemovalPolicy.DESTROY,  # Secure: auto-deletes on stack update
            auto_delete_objects=True,
            block_public_access=s3.BlockPublicAccess.BLOCK_ALL,
            public_read_access=False,
            website_index_document="index.html",
            website_error_document="error.html",
            cors_configuration=s3.CorsConfiguration(
                max_age_seconds=300,
                cors_rules=[
                    s3.CorsRule(
                        allowed_headers=["Authorization", "Content-Type"],
                        allowed_methods=[s3.CorsHttpMethod.GET, s3.CorsHttpMethod.HEAD],
                        allowed_origins=["*"],
                        expose_headers=["x-amz-server-side-encryption"],
                        max_stored_items=1000
                    )
                ]
            )
        )