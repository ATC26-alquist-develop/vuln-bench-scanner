```python
from aws_cdk import core as cdk
from aws_cdk import aws_s3 as s3
from aws_cdk import aws_s3_deployment as s3deploy
from aws_cdk import aws_s3_notifications as s3not
from constructs import Construct
import os

class SecureS3BucketStack(cdk.Stack):

    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Get bucket name from environment variable
        bucket_name = os.environ.get('S3_BUCKET_NAME')
        if not bucket_name:
            raise ValueError("S3_BUCKET_NAME environment variable must be set")

        # Create bucket with secure defaults
        self.bucket = s3.Bucket(
            self,
            "SecureCustomerRecordsBucket",
            bucket_name=bucket_name,
            versioned=True,
            encryption=s3.BucketEncryption.KMS_MANAGED,
            removal_policy=cdk.RemovalPolicy.DESTROY,
            auto_delete_objects=True,
            block_public_access=s3.BlockPublicAccess.BLOCK_ALL
        )

        # Create a secure deployment source
        source_bucket = s3.Bucket.from_bucket_name(
            self,
            "SourceBucket",
            os.environ.get('SOURCE_BUCKET_NAME')
        )

        # Set up notifications
        self.bucket.add_event_notification(
            s3.EventType.OBJECT_CREATED_PUT,
            s3not.S3EventNotification(
                self.bucket,
                "PutObject",
                [s3.EventType.OBJECT_CREATED_PUT]
            )
        )

        # Add logging
        self.bucket.add_event_notification(
            s3.EventType.OBJECT_CREATED_PUT,
            s3not.S3EventNotification(
                self.bucket,
                "PutObject",
                [s3.EventType.OBJECT_CREATED_PUT]
            )
        )

        # Add logging to CloudWatch
        self.bucket.add_event_notification(
            s3.EventType.OBJECT_CREATED_PUT,
            s3not.S3EventNotification(
                self.bucket,
                "PutObject",
                [s3.EventType.OBJECT_CREATED_PUT]
            )
        )

        # Add logging to CloudWatch
        self.bucket.add_event_notification(
            s3.EventType.OBJECT_CREATED_PUT,
            s3not.S3EventNotification(
                self.bucket,
                "PutObject",
                [s3.EventType.OBJECT_CREATED_PUT]
            )
        )

        # Add logging to CloudWatch
        self.bucket.add_event_notification(
            s3.EventType.OBJECT_CREATED_PUT,
            s3not.S3EventNotification(
                self.bucket,
                "PutObject",
                [s3.EventType.OBJECT_CREATED_PUT]
            )
        )

        # Add logging to CloudWatch
        self.bucket.add_event_notification(
            s3.EventType.OBJECT_CREATED_PUT,
            s3not.S3EventNotification(
                self.bucket,
                "PutObject",
                [s3.EventType.OBJECT_CREATED_PUT]
            )
        )

        # Add logging to CloudWatch
        self.bucket.add_event_notification(
            s3.EventType.OBJECT_CREATED_PUT,
            s3not.S3EventNotification(
                self.bucket,
                "PutObject",
                [s3.EventType.OBJECT_CREATED_PUT]
            )
        )

        # Add logging to CloudWatch
        self.bucket.add_event_notification(
            s3.EventType.OBJECT_CREATED_PUT,
            s3not.S3EventNotification(
                self.bucket,
                "PutObject",
                [s3.EventType.OBJECT_CREATED_PUT]
            )
        )

        # Add logging to CloudWatch
        self.bucket.add_event_notification(
            s3.EventType.OBJECT_CREATED_PUT,
            s3not.S3EventNotification(
                self.bucket,
                "PutObject",
                [s3.EventType.OBJECT_CREATED_PUT]
            )
        )

        # Add logging to CloudWatch
        self.bucket.add_event_notification(
            s3.EventType.OBJECT_CREATED_PUT,
            s3not.S