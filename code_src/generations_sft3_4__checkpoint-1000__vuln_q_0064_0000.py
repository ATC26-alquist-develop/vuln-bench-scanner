from aws_cdk import core
from aws_cdk.aws_s3 import Bucket
from aws_cdk.aws_s3_deployment import BucketDeployment
from aws_cdk.aws_s3_deployment import Source
from aws_cdk import aws_s3 as s3
from aws_cdk import aws_s3_deployment as s3deploy
from aws_cdk import aws_iam as iam
import os

class SimpleS3BucketStack(core.Stack):

    def __init__(self, app: core.App, id: str, **kwargs) -> None:
        super().__init__(app, id, **kwargs)

        # Get bucket name from environment variable
        bucket_name = os.environ.get('S3_BUCKET_NAME')
        if not bucket_name:
            raise ValueError("S3_BUCKET_NAME environment variable must be set")

        # Create bucket with secure defaults
        self.bucket = s3.Bucket(
            self,
            "SecureBucket",
            bucket_name=bucket_name,
            versioned=True,
            encryption=s3.BucketEncryption.S3_MANAGED,
            removal_policy=core.RemovalPolicy.DESTROY
        )

        # Create deployment source
        source = Source.asset('static_content')

        # Deploy content to bucket
        s3deploy.BucketDeployment(
            self,
            "DeployContent",
            sources=[source],
            destination_bucket=self.bucket
        )

        # Add basic access logging
        self.bucket.add_event_notification(
            s3.EventType.OBJECT_CREATED_PUT,
            s3.NotificationTarget(
                target=s3.BucketLoggingConfiguration(
                    bucket=self.bucket,
                    log_group_name=f"/aws/s3/{self.bucket.bucket_name}/log",
                    prefix="s3-logs/"
                )
            )
        )

        # Add basic access policy
        self.bucket.add_to_resource_policy(
            iam.PolicyStatement(
                effect=iam.Effect.ALLOW,
                principals=[iam.AnyPrincipal()],
                actions=["s3:GetObject"],
                resources=[f"{self.bucket.bucket_arn}/*"]
            )
        )

        # Add default error handling
        self.bucket.add_to_resource_policy(
            iam.PolicyStatement(
                effect=iam.Effect.ALLOW,
                principals=[iam.AnyPrincipal()],
                actions=["s3:PutObject"],
                resources=[f"{self.bucket.bucket_arn}/*"]
            )
        )

        # Add default CORS configuration
        self.bucket.add_cors_rule(
            allowed_methods=[s3.HttpMethod.GET, s3.HttpMethod.PUT, s3.HttpMethod.POST],
            allowed_origins=["*"],
            max_age_seconds=3000
        )

# Usage example
app = core.App()
SimpleS3BucketStack(app, "SimpleS3Bucket")
app.synth()