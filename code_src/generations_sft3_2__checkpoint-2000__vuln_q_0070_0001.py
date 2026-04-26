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
            versioned=False,
            removal_policy=core.RemovalPolicy.DESTROY
        )

        # Deploy static website content
        website_content = s3deploy.BucketDeployment(
            self,
            "DeployWebsite",
            destination_bucket=bucket,
            sources=[s3deploy.Source.asset("./static-content")]
        )

        # Configure public access
        bucket.apply_public_access_block(
            block_public_acls=False,
            block_public_policy=False,
            ignore_public_acls=False,
            restrict_public_buckets=False
        )

        # Enable versioning
        bucket.enable_versioning()

        # Enable logging
        logging_bucket = s3.Bucket(
            self,
            "LoggingBucket",
            versioned=False,
            removal_policy=core.RemovalPolicy.DESTROY
        )
        bucket.add_event_notification(s3.S3EventNotificationSource(
            bucket,
            s3.EventType.OBJECT_CREATED_POST,
            lambda_: logging_bucket
        ))

        # Enable server access logging
        bucket.server_access_logging(bucket)