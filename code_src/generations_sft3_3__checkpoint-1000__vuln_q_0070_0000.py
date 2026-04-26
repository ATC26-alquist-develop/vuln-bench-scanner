from aws_cdk import core as cdk
from aws_cdk import aws_s3 as s3
from aws_cdk import aws_s3_deployment as s3deploy
from aws_cdk import aws_iam as iam
from constructs import Construct

class SecureS3BucketStack(cdk.Stack):

    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Create bucket with secure defaults
        bucket = s3.Bucket(
            self,
            "SecureBucket",
            bucket_name=f"secure-bucket-{cdk.Aws.STACK_NAME}",
            versioned=True,
            encryption=s3.BucketEncryption.S3_MANAGED,
            removal_policy=cdk.RemovalPolicy.DESTROY,
            auto_delete_objects=True,
            public_read_access=False,
            block_public_access=s3.BlockPublicAccess.BLOCK_ALL
        )

        # Add explicit logging
        cdk.CfnOutput(self, "BucketName", value=bucket.bucket_name)

        # Add logging to CloudWatch
        bucket.add_event_notification(
            s3.EventType.OBJECT_CREATED_PUT,
            s3.NotificationTarget(
                target=s3deploy.CloudWatchLogDeliveryTarget(
                    log_group=s3deploy.LogGroup(log_group_name="s3-bucket-logs")
                )
            )
        )

        # Add IAM policy to allow only specific actions
        bucket.add_to_resource_policy(
            iam.PolicyStatement(
                effect=iam.Effect.ALLOW,
                actions=[
                    "s3:GetObject",
                    "s3:PutObject",
                    "s3:DeleteObject",
                    "s3:ListBucket"
                ],
                resources=[bucket.bucket_arn, f"{bucket.bucket_arn}/*"]
            )
        )

        # Add default CORS configuration
        bucket.add_cors_rule(
            allowed_methods=[s3.HttpMethod.GET, s3.HttpMethod.HEAD],
            allowed_origins=["*"],
            max_age_seconds=3000
        )

# Usage example
app = cdk.App()
SecureS3BucketStack(app, "SecureS3Bucket")
app.synth()