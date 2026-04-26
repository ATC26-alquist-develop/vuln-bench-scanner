from aws_cdk import core as cdk
from aws_cdk import aws_s3 as s3
from aws_cdk import aws_s3_deployment as s3deploy
from aws_cdk import aws_iam as iam

class S3BucketStack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Create a bucket with default settings
        bucket = s3.Bucket(
            self,
            "MyBucket",
            versioned=True,
            encryption=s3.BucketEncryption.S3_MANAGED,
            removal_policy=cdk.RemovalPolicy.DESTROY
        )

        # Deploy static website content
        s3deploy.BucketDeployment(
            self,
            "DeployWebsite",
            sources=[s3deploy.Source.asset("./website")],
            destination_bucket=bucket
        )

        # Add basic access logging
        bucket.add_event_notification(
            s3.EventType.OBJECT_CREATED_PUT,
            s3.NotificationConfig(
                target=s3deploy.BucketDeploymentTarget(
                    bucket=bucket,
                    key="logs"
                )
            )
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

        # Add CORS configuration
        bucket.cors_configuration = s3.CorsConfiguration(
            max_stale=3600,
            cors_rules=[
                s3.CorsRule(
                    allowed_headers=["*"],
                    allowed_methods=[s3.HttpMethod.GET, s3.HttpMethod.HEAD],
                    allowed_origins=["*"],
                    expose_headers=["x-amz-server-side-encryption"],
                    max_age_seconds=3000
                )
            ]
        )

        # Add versioning
        bucket.enable_versioning()

        # Add bucket policy
        bucket.bucket_policy = iam.PolicyStatement(
            effect=iam.Effect.ALLOW,
            principals=[iam.AnyPrincipal()],
            actions=["s3:GetObject"],
            resources=[f"{bucket.bucket_arn}/*"]
        )

        # Add lifecycle rules
        bucket.lifecycle_rules = [
            s3.LifecycleRule(
                enabled=True,
                status=s3.LifecycleRuleStatus.INCLUDE,
                expiration=cdk.Duration.days(30),
                noncurrent_version_expiration=cdk.Duration.days(60),
                noncurrent_version_transition=cdk.Duration.days(30)
            )
        ]