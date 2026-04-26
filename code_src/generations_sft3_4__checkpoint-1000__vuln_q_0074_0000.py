from aws_cdk import core
from aws_cdk.aws_s3 import Bucket, BucketEncryption
from aws_cdk.aws_kms import Key
from aws_cdk import aws_kms as _kms

class SecureS3BucketStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Create a KMS key for encryption
        self.encryption_key = Key(self, "SecureEncryptionKey",
            description="Secure S3 bucket encryption key",
            enable_key_rotation=True,
            encryption_context={
                "aws:cdk:construct-type": "SecureS3BucketStack"
            }
        )

        # Create S3 bucket with encryption
        self.bucket = Bucket(self, "SecureBucket",
            bucket_name=f"secure-bucket-{self.region}-{self.account}",
            encryption=BucketEncryption.KMS,
            encryption_key=self.encryption_key,
            removal_policy=core.RemovalPolicy.DESTROY,
            versioned=True,
            auto_delete_objects=True
        )

        # Add additional security measures
        self.bucket.add_to_resource_policy(
            core.PolicyStatement(
                actions=["s3:GetBucketPolicy"],
                principals=[core.AccountPrincipal("allUsers")],
                resources=[self.bucket.bucket_arn]
            )
        )

        # Add logging for security events
        self.bucket.add_event_notification(
            core.EventSource.MARKETPLACED_EVENTS,
            core.NotificationTarget(self, "SecurityEvents",
                target=core.CfnOutput(
                    self,
                    "SecurityEventsLogGroup",
                    value=self.bucket.log_group.log_group_arn
                )
            )
        )