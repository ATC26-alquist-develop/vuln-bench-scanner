from aws_cdk import core as cdk
from aws_cdk import aws_s3 as s3
from constructs import Construct

class SecureS3BucketStack(cdk.Stack):

    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Create a secure S3 bucket with default policies
        bucket = s3.Bucket(
            self,
            "SecureBucket",
            bucket_name=f"secure-bucket-{cdk.Aws.RandomValueGenerator.generate().string(8)}",
            versioned=True,
            encryption=s3.BucketEncryption.KMS_MANAGED,
            removal_policy=cdk.RemovalPolicy.DESTROY,  # Secure: auto-deletes on stack update
            auto_delete_objects=True,  # Secure: automatically deletes objects on bucket deletion
            block_public_access=s3.BlockPublicAccess.BLOCK_ALL,
            public_read_access=False,
            auto_delete_objects_versioned=True
        )

        # Add any additional secure configurations here
        # For example, you can add logging to CloudWatch
        logging_bucket = s3.Bucket(
            self,
            "LoggingBucket",
            bucket_name=f"logging-bucket-{cdk.Aws.RandomValueGenerator.generate().string(8)}",
            versioned=True,
            encryption=s3.BucketEncryption.KMS_MANAGED,
            removal_policy=cdk.RemovalPolicy.DESTROY,
            block_public_access=s3.BlockPublicAccess.BLOCK_ALL,
            public_read_access=False
        )

        # Add CloudWatch logging to the S3 bucket
        bucket.add_event_notification(
            s3.EventNotificationSource(bucket),
            s3.S3EventNotification.AllEvents,
            s3.NotificationConfig(log_bucket=logging_bucket)
        )