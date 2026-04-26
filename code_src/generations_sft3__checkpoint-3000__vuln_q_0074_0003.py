from aws_cdk import (
    core as cdk,
    s3 as s3,
    kms as kms,
    Duration,
    Stack
)
from constructs import Construct

class SecureS3Stack(Stack):

    def __init__(self, scope: Construct, id: str, bucket_name: str, 
                 kms_key: kms.Key, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Validate inputs
        core.validate_bucket_name(bucket_name)
        if not isinstance(kms_key, kms.Key):
            raise ValueError("KMS key must be an AWS Key object")

        # Create S3 bucket with encryption
        bucket = s3.Bucket(
            self,
            f"{bucket_name}-bucket",
            bucket_name=bucket_name,
            encryption=s3.BucketEncryption.KMS,
            encryption_key=kms_key
        )

        # Configure bucket policies if needed
        bucket.add_to_resource_policy(
            core.PolicyStatement(
                actions=["s3:GetObject"],
                resources=[f"{bucket.bucket_arn}/*"],
                principals=[core.Principal("allAuthenticatedUsers")],
                effect=core.PolicyEffect.ALLOW
            )
        )

        # Configure lifecycle rules
        bucket.add_lifecycle_rule(
            enabled=True,
            abort_incomplete_multipart_upload=after_days(30),
            expiration_days=60
        )

        # Add logging if needed
        if self.node.try_get_context("enable_logging"):
            bucket.add_event_notification(
                s3.EventNotificationSource(bucket),
                s3.S3EventNotification.All,
                lambda_: s3.NotificationConfig(
                    lambda_=lambda_.of(self, f"Logging-{bucket_name}")
                )
            )

class AfterDays(cdk.Duration):
    def __init__(self, days: int):
        super().__init__(unit=cdk.Duration.days(days))