from aws_cdk import (
    core,
    aws_s3 as s3,
    aws_s3_deployment as s3deploy,
    aws_s3_bucket_public_access as bucket_public_access
)

class S3BucketStack(core.Stack):

    def __init__(self, app: core.App, id: str, **kwargs) -> None:
        super().__init__(app, id, **kwargs)

        # Create a new S3 bucket
        bucket = s3.Bucket(
            self,
            "MyWebAppBucket",
            versioned=True,
            encryption=s3.BucketEncryption.S3_MANAGED,
            removal_policy=core.RemovalPolicy.DESTROY
        )

        # Deploy static website content
        s3deploy.BucketDeployment(
            self,
            "DeployWebsite",
            sources=[s3deploy.Source.asset("./static_content")],
            destination_bucket=bucket
        )

        # Configure public access
        bucket.add_public_access_block(
            block_public_acls=False,
            block_public_policy=False,
            ignore_public_acls=False,
            restrict_public_buckets=False
        )

        # Enable versioning
        bucket.enable_versioning()

        # Enable logging
        bucket.add_to_resource_policy(
            core.PolicyStatement(
                actions=["s3:PutObject"],
                resources=[f"{bucket.bucket_arn}/*"],
                principals=[core.Principal("logdelivery.amazonaws.com")],
                effect=core.PolicyEffect.ALLOW
            )
        )

        # Enable bucket logging
        bucket.logging_enabled(
            log_bucket=bucket,
            log_prefix="website-logs"
        )