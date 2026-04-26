import os
from aws_cdk import core
from s3 import S3Bucket
from s3_deployment import (
    S3Deploy,
    WebsiteConfig
)
from constructs import Construct

class SecureS3BucketStack(core.Stack):

    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Get bucket name from environment variable
        bucket_name = os.environ.get('S3_BUCKET_NAME')
        if not bucket_name:
            raise ValueError("S3_BUCKET_NAME environment variable must be set")

        # Create bucket with secure defaults
        self.bucket = S3Bucket(
            self,
            "SecureBucket",
            bucket_name=bucket_name,
            versioned=True,
            encryption=S3BucketEncryptionOptions.SSEKMS,
            removal_policy=core.RemovalPolicy.DESTROY
        )

        # Configure website hosting
        website_config = WebsiteConfig(
            index_document="index.html",
            error_document="error.html",
            cors=[
                core.CfnBucket.CorsRuleProperty(
                    allowed_headers=["*"],
                    allowed_methods=["GET", "HEAD"],
                    expose_headers=["*"],
                    max_age_seconds=300
                )
            ]
        )

        self.bucket.add_to_resource_policy(
            core.PolicyStatement(
                actions=["s3:GetObject"],
                resources=[f"{self.bucket.bucket_arn}/*"],
                principals=[core.PolicyPrincipal(principal_type="Group", principal="allUsers")]
            )
        )

        # Deploy static content
        S3Deploy(
            self,
            "StaticContent",
            bucket=self.bucket,
            source_dir="static_content",
            website_config=website_config
        )