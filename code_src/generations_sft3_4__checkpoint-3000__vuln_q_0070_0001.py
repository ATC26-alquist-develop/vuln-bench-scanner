from aws_cdk import (
    core,
    aws_s3 as s3,
    aws_s3_deployment as s3deploy,
    aws_s3_bucket_public_access as bucket_public_access
)

class S3BucketStack(core.Stack):
    def __init__(self, app: core.App, id: str, **kwargs) -> None:
        super().__init__(app, id, **kwargs)
        
        # Create a new S3 bucket
        bucket = s3.Bucket(
            self,
            "MyWebAppBucket",
            bucket_name=f"my-web-app-bucket-{core.Stack.of(self).generate_unique_name('stack-')}",
            removal_policy=core.RemovalPolicy.DESTROY  # For demonstration only, use RETAIN in production
        )

        # Deploy static website content
        s3deploy.BucketDeployment(
            self,
            "DeployWebsite",
            sources=[s3deploy.Source.asset("./static-content")],
            destination_bucket=bucket
        )

        # Configure public access
        bucket.add_to_resource_policy(
            core.PolicyStatement(
                actions=["s3:GetObject"],
                resources=[f"{bucket.bucket_arn}/*"],
                principals=[core.Principal("allAuthenticatedUsers")],
                effect=core.PolicyEffect.ALLOW
            )
        )

        # Restrict access to specific IPv4 CIDR
        bucket.add_to_resource_policy(
            core.PolicyStatement(
                actions=["s3:GetObject"],
                resources=[f"{bucket.bucket_arn}/*"],
                principals=[core.Principal("AWS:arn:aws:iam::123456789012:root")],
                effect=core.PolicyEffect.ALLOW,
                conditions={
                    "IpAddress": {
                        "aws:SourceIp": "192.0.2.0/24"
                    }
                }
            )
        )

        # Enable versioning
        bucket.versioning_enabled = True

        # Enable server access logging
        bucket.logging_enabled = s3.LoggingConfig(
            log_file_prefix="logs/",
            destination_bucket=bucket
        )