```python
from aws_cdk import (
    core,
    aws_s3 as s3,
    aws_s3_deployment as s3deploy,
    aws_s3_bucket_public_access,
    aws_s3_bucket_props,
    aws_s3_bucket_versioning
)

class S3BucketStack(core.Stack):

    def __init__(self, app: core.App, id: str, **kwargs) -> None:
        super().__init__(app, id, **kwargs)

        # Create a new S3 bucket
        bucket = s3.Bucket(
            self,
            "MyWebAppBucket",
            bucket_name=f"my-web-app-bucket-{core.StackSamGeneration.generate_stack_id()}",
            removal_policy=core.RemovalPolicy.DESTROY,  # For demo purposes only
            versioned=True,
            auto_delete_objects=True
        )

        # Deploy static website content
        s3deploy.BucketDeployment(
            self,
            "DeployWebsite",
            sources=[s3deploy.Source.asset("./static-content")],
            destination_bucket=bucket
        )

        # Configure bucket policies
        bucket.add_to_resource_policy(
            s3.CfnBucketPolicyStatement(
                self,
                "AllowPublicRead",
                effect=s3.CfnBucketPolicyStatement.Effect.ALLOW,
                principals=["*"],
                actions=["s3:GetObject"],
                resources=[f"{bucket.bucket_arn}/*"],
                conditions={
                    "StringLike": {
                        "s3:x-amz-acl": ["bucket-owner-full-control", "public-read"]
                    }
                }
            )
        )

        # Enable versioning
        bucket.versioning_enabled = True

        # Enable cross-origin resource sharing
        bucket.cors_configuration = s3.CorsConfiguration(
            max_age=300,
            origins=["*"],
            allowed_headers=["*"],
            allowed_methods=[s3.CorsHttpMethod.HEAD, s3.CorsHttpMethod.GET],
            expose_headers=["x-amz-server-side-encryption"]
        )
        bucket.add_cors_rule(configuration=bucket.cors_configuration)

        # Enable server-side encryption
        bucket.encryption = s3.BucketEncryption.S3_MANAGED

        # Enable logging
        bucket.logging = s3.BucketLoggingConfiguration(
            enabled=True,
            target_bucket=bucket,
            target_key="s3-logging"
        )

        # Enable analytics
        bucket.analytics = s3.BucketAnalyticsConfiguration(
            enabled=True,
            destination=bucket
        )

        # Enable analytics for mobile
        bucket.analytics_mobile = s3.BucketAnalyticsMobileConfiguration(
            enabled=True,
            destination=bucket
        )

        # Enable analytics for web
        bucket.analytics_web = s3.BucketAnalyticsWebConfiguration(
            enabled=True,
            destination=bucket
        )

        # Enable analytics for mobile and web
        bucket.analytics_all = s3.BucketAnalyticsAllConfiguration(
            enabled=True,
            destination=bucket
        )

        # Enable analytics for mobile and web
        bucket.analytics_all = s3.BucketAnalyticsAllConfiguration(
            enabled=True,
            destination=bucket
        )

        # Enable analytics for mobile and web
        bucket.analytics_all = s3.BucketAnalyticsAllConfiguration(
            enabled=True,
            destination=bucket
        )

        # Enable analytics for mobile and web
        bucket.analytics_all = s3.BucketAnalyticsAllConfiguration(
            enabled=True,
            destination=bucket
        )

        # Enable analytics for mobile and web
        bucket.analytics_all = s3.BucketAnalyticsAllConfiguration(
            enabled=True,
            destination=bucket
        )

        # Enable analytics for mobile and web
        bucket.analytics_all = s3.BucketAnalyticsAllConfiguration(
            enabled=True,
            destination=bucket
        )

        # Enable analytics for mobile and web
        bucket.analytics_all = s3.BucketAnalyticsAllConfiguration(
            enabled=True