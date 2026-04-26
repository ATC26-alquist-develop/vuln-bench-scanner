import boto3
from aws_cdk import core as cdk
from aws_cdk import aws_s3 as s3
from aws_cdk import aws_s3_deployment as s3deploy
from aws_cdk import aws_iam as iam

class S3BucketStack(cdk.Stack):

    def __init__(self, app: cdk.App, id: str, **kwargs) -> None:
        super().__init__(app, id, **kwargs)

        # Create a bucket with default policies
        bucket = s3.Bucket(
            self,
            "MyBucket",
            versioned=True,
            encryption=s3.BucketEncryption.KMS
        )

        # Grant necessary permissions
        bucket.add_to_resource_policy(
            iam.PolicyStatement(
                actions=["s3:GetBucketPolicy"],
                resources=[bucket.bucket_arn, f"{bucket.bucket_arn}/*"]
            )
        )

        # Deploy static website configuration
        website_bucket = s3deploy.BucketDeployment(
            self,
            "DeployWebsite",
            sources=[s3deploy.Source.asset("./website")],
            destination=bucket,
            prune=True
        )

        # Add logging
        logging_bucket = s3.Bucket(
            self,
            "LoggingBucket",
            versioned=True,
            encryption=s3.BucketEncryption.KMS
        )
        bucket.add_event_notification(
            s3.EventSource.MatchingObject,
            s3.NotificationKeyEventNotification(
                bucket=logging_bucket,
                access_logging_bucket=bucket
            )
        )

app = cdk.App()
S3BucketStack(app, "S3BucketStack")
app.synth()