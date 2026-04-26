```python
from aws_cdk import core as cdk
from aws_cdk import aws_s3 as s3
from aws_cdk import aws_s3_deployment as s3deploy
from aws_cdk import aws_iam as iam
from constructs import Construct

class SimpleS3BucketStack(cdk.Stack):

    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Create a bucket with secure defaults
        bucket = s3.Bucket(
            self,
            "SecureBucket",
            bucket_name=f"secure-bucket-{cdk.Aws.STACK_NAME}",
            versioned=False,  # Disable versioning for simplicity
            encryption=s3.BucketEncryption.S3_MANAGED,
            removal_policy=cdk.RemovalPolicy.DESTROY,  # Remove on stack update
            auto_delete_objects=True,  # Enable auto-deletion
            block_public_access=s3.BlockPublicAccess.BLOCK_ALL,
            public_read_access=False,
            cors=[s3.CorsRule(
                allowed_headers=["*"],
                allowed_methods=[s3.HttpMethod.GET, s3.HttpMethod.PUT],
                allowed_origins=["*"],
                max_age_seconds=300
            )]
        )

        # Add basic access logging
        bucket.add_cors_rule(
            allowed_headers=["*"],
            allowed_methods=[s3.HttpMethod.GET, s3.HttpMethod.PUT],
            allowed_origins=["*"],
            max_age_seconds=300
        )

        # Add basic access policy
        bucket.add_to_resource_policy(
            iam.PolicyStatement(
                effect=iam.Effect.ALLOW,
                principals=[iam.AnyPrincipal()],
                actions=["s3:GetObject"],
                resources=[f"{bucket.bucket_arn}/*"]
            )
        )

        # Add basic logging
        bucket.add_event_notification(
            s3.EventType.OBJECT_CREATED_PUT,
            s3.NotificationConfig(
                target=s3deploy.BucketDeployment(
                    sources=[s3deploy.Source.asset("./logs")],
                    destination_bucket=bucket
                )
            )
        )

        # Add basic access logging
        bucket.add_event_notification(
            s3.EventType.OBJECT_CREATED_PUT,
            s3.NotificationConfig(
                target=s3deploy.BucketDeployment(
                    sources=[s3deploy.Source.asset("./logs")],
                    destination_bucket=bucket
                )
            )
        )

        # Add basic access logging
        bucket.add_event_notification(
            s3.EventType.OBJECT_CREATED_PUT,
            s3.NotificationConfig(
                target=s3deploy.BucketDeployment(
                    sources=[s3deploy.Source.asset("./logs")],
                    destination_bucket=bucket
                )
            )
        )

        # Add basic access logging
        bucket.add_event_notification(
            s3.EventType.OBJECT_CREATED_PUT,
            s3.NotificationConfig(
                target=s3deploy.BucketDeployment(
                    sources=[s3deploy.Source.asset("./logs")],
                    destination_bucket=bucket
                )
            )
        )

        # Add basic access logging
        bucket.add_event_notification(
            s3.EventType.OBJECT_CREATED_PUT,
            s3.NotificationConfig(
                target=s3deploy.BucketDeployment(
                    sources=[s3deploy.Source.asset("./logs")],
                    destination_bucket=bucket
                )
            )
        )

        # Add basic access logging
        bucket.add_event_notification(
            s3.EventType.OBJECT_CREATED_PUT,
            s3.NotificationConfig(
                target=s3deploy.BucketDeployment(
                    sources=[s3deploy.Source.asset("./logs")],
                    destination_bucket=bucket
                )
            )
        )

        # Add basic access logging
        bucket.add_event_notification(
            s3.EventType.OBJECT_CREATED_PUT,
            s3.NotificationConfig(
                target=s3deploy.BucketDeployment(
                    sources=[s3deploy.Source.asset("./logs")],
                    destination