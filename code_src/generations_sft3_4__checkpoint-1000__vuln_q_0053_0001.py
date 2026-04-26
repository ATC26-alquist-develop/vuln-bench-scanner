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
            encryption=s3.BucketEncryption.S3_MANAGED,
            removal_policy=cdk.RemovalPolicy.DESTROY,
            auto_delete_objects=True,
            block_public_access=s3.BlockPublicAccess.BLOCK_ALL
        )

        # Create a secure website endpoint
        self.bucket.add_public_access_block()

        # Set up notifications
        self.bucket.add_event_notification(
            s3.EventType.OBJECT_CREATED_PUT,
            s3not.S3EventNotification(self.bucket, "CustomerRecordsCreated", actions=["s3:ObjectCreated:*"])
        )

        # Add logging
        self.bucket.add_event_notification(
            s3.EventType.OBJECT_CREATED_PUT,
            s3not.S3EventNotification(self.bucket, "CustomerRecordsCreated", actions=["logs:PutLogEvents"])
        )

        # Set up CORS
        self.bucket.cors(
            [
                s3.CorsRule(
                    allowed_headers=["Authorization"],
                    allowed_methods=[s3.HttpMethod.PUT, s3.HttpMethod.POST],
                    allowed_origins=["https://example.com"],
                    exposed_headers=["ETag"],
                    max_age_seconds=300
                )
            ]
        )

        # Set up bucket policy
        self.bucket.add_to_resource_policy(
            s3.CfnBucketPolicy.StatementProperty(
                effect=s3.CfnBucketPolicy.StatementEffect.DENY,
                principals=["*"],
                actions=["s3:*"],
                resources=[f"arn:aws:s3:::{self.bucket.bucket_name}/*"],
                conditions=[
                    {
                        "StringLike": {
                            "s3:x-amz-acl": ["private"]
                        }
                    }
                ]
            )
        )

        # Set up versioning
        self.bucket.enable_versioning()

        # Set up lifecycle rules
        self.bucket.add_lifecycle_rule(
            enabled=True,
            expiration=cdk.Duration.days(365),
            abort_incomplete_multipart_upload_after=cdk.Duration.days(30)
        )

        # Set up bucket policy
        self.bucket.add_to_resource_policy(
            s3.CfnBucketPolicy.StatementProperty(
                effect=s3.CfnBucketPolicy.StatementEffect.DENY,
                principals=["*"],
                actions=["s3:*"],
                resources=[f"arn:aws:s3:::{self.bucket.bucket_name}/*"],
                conditions=[
                    {
                        "StringLike": {
                            "s3:x-amz-acl": ["private"]
                        }
                    }
                ]
            )
        )

        # Set up bucket policy
        self.bucket.add_to_resource_policy(
            s3.CfnBucketPolicy.StatementProperty(
                effect=s3.CfnBucketPolicy.StatementEffect.DENY,
                principals=["*"],
                actions=["s3:*"],
                resources=[f"arn:aws:s3:::{self.bucket.bucket_name}/*"],
                conditions=[
                    {
                        "StringLike": {
                            "s3:x-amz-acl": ["private"]
                        }
                    }
                ]
            )
        )

        # Set up bucket