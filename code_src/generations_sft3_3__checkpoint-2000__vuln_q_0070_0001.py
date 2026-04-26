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
            sources=[s3deploy.Source.asset("./static-content")],
            destination_bucket=bucket
        )

        # Configure public access
        bucket.add_public_access_block()

        # Add logging
        logging_bucket = s3.Bucket(
            self,
            "LoggingBucket",
            versioned=True,
            encryption=s3.BucketEncryption.S3_MANAGED,
            removal_policy=core.RemovalPolicy.DESTROY
        )
        bucket.logging_enabled = s3.LoggingConfig(
            log_bucket=logging_bucket,
            log_prefix="s3-logging"
        )

        # Restrict access to the bucket
        bucket.apply_main_policy()

# Usage
app = core.App()
S3BucketStack(app, "S3BucketStack")
app.synth()