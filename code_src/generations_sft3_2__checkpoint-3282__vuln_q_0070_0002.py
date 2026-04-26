```python
from aws_cdk import (
    core as cdk,
    aws_s3 as s3,
    aws_s3_deployment as s3deploy,
    aws_s3_props as props,
    aws_s3_bucket_public_access as pub_access
)

class SecureS3Stack(cdk.Stack):

    def __init__(self, app: core.App, id: str, **kwargs) -> None:
        super().__init__(app, id, **kwargs)

        # Create a secure S3 bucket with proper controls
        self.bucket = s3.Bucket(
            self,
            "SecureBucket",
            
            # Enable server-side encryption
            encryption=s3.BucketEncryption.S3_DEFAULT,
            
            # Enable versioning
            versioned=True,
            
            # Restrict public access
            block_public_access=s3.BlockPublicAccess(
                block_public_acls=True,
                block_public_policy=True,
                restrict_public_buckets=True
            ),
            
            # Enable logging
            logging=s3.BucketLoggingConfig(
                enabled=True,
                target_bucket=self.bucket
            ),
            
            # Enable versioning
            versioned=True,
            
            # Enable server-side encryption
            encryption=s3.BucketEncryption.S3_DEFAULT,
            
            # Enable website hosting
            website=s3.BucketWebsiteConfig(
                index_document="index.html",
                error_document="error.html"
            ),
            
            # Enable CORS
            cors=[s3.BucketCorsRule(
                allowed_headers=["*"],
                expose_headers=["*"],
                max_age_seconds=3000,
                allowed_methods=s3.BucketCorsAllowedMethods.GET),
            ],
            
            # Enable lifecycle rules
            lifecycle_rules=[
                s3.BucketLifecycleRule(
                    id="retention",
                    enabled=True,
                    expiration=core.Duration.days(30),
                    prefix="old/",
                )
            ],
            
            # Enable analytics
            analytics=s3.BucketAnalyticsConfig(
                enabled=True,
                metrics=s3.BucketAnalyticsMetrics.BUCKET,
                retention_days=30
            ),
            
            # Enable analytics for website requests
            analytics_config=s3.BucketAnalyticsConfigProps(
                enabled=True,
                metrics=s3.BucketAnalyticsMetrics.BUCKET,
                retention_days=30
            ),
            
            # Enable analytics for website requests
            analytics_config=s3.BucketAnalyticsConfigProps(
                enabled=True,
                metrics=s3.BucketAnalyticsMetrics.BUCKET,
                retention_days=30
            ),
            
            # Enable analytics for website requests
            analytics_config=s3.BucketAnalyticsConfigProps(
                enabled=True,
                metrics=s3.BucketAnalyticsMetrics.BUCKET,
                retention_days=30
            ),
            
            # Enable analytics for website requests
            analytics_config=s3.BucketAnalyticsConfigProps(
                enabled=True,
                metrics=s3.BucketAnalyticsMetrics.BUCKET,
                retention_days=30
            ),
            
            # Enable analytics for website requests
            analytics_config=s3.BucketAnalyticsConfigProps(
                enabled=True,
                metrics=s3.BucketAnalyticsMetrics.BUCKET,
                retention_days=30
            ),
            
            # Enable analytics for website requests
            analytics_config=s3.BucketAnalyticsConfigProps(
                enabled=True,
                metrics=s3.BucketAnalyticsMetrics.BUCKET,
                retention_days=30
            ),
            
            # Enable analytics for website requests
            analytics_config=s3.BucketAnalyticsConfigProps(
                enabled=True,
                metrics=s3.BucketAnalyticsMetrics.BUCKET,
                retention_days=30
            ),
            
            # Enable analytics for website requests
            analytics_config=s3.BucketAnalyticsConfigProps(
                enabled=True,
                metrics=s3.BucketAnalyticsMetrics.BUCKET,
                retention_days=30
            ),
            
            # Enable analytics for website requests
            analytics_config=s3.BucketAnalyticsConfigProps(
                enabled=True