```python
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
            bucket_name=f"secure-bucket-{cdk.Aws.RandomValueGenerator.generate().string(8)}",
            versioned=False,
            encryption=s3.BucketEncryption.S3_MANAGED,
            block_public_access=s3.BlockPublicAccess.BLOCK_ALL,
            removal_policy=cdk.RemovalPolicy.DESTROY
        )

        # Add explicit logging
        bucket.add_to_resource_policy(
            iam.PolicyStatement(
                effect=iam.Effect.ALLOW,
                principals=[iam.AnyPrincipal()],
                actions=["s3:PutObject"],
                resources=[f"{bucket.bucket_arn}/*"],
                conditions={
                    "StringLike": {
                        "s3:x-amz-acl": ["bucket-owner-full-control"]
                    }
                }
            )
        )

        # Add explicit access logging
        bucket.add_event_notification(
            s3.EventType.OBJECT_CREATED_PUT,
            s3.NotificationConfig(
                target=s3deploy.BucketDeployment(
                    sources=[s3deploy.Source.asset("./static-content")],
                    destination_bucket=bucket
                )
            )
        )

        # Add explicit CORS configuration
        bucket.add_cors_rule(
            allowed_headers=["*"],
            allowed_methods=[s3.HttpMethod.GET, s3.HttpMethod.HEAD],
            allowed_origins=["*"],
            max_age_seconds=3000
        )

        # Add explicit access control
        bucket.add_to_resource_policy(
            iam.PolicyStatement(
                effect=iam.Effect.ALLOW,
                principals=[iam.AnyPrincipal()],
                actions=["s3:GetBucketAcl"],
                resources=[bucket.bucket_arn]
            )
        )

        # Add explicit bucket policy
        bucket.add_to_resource_policy(
            iam.PolicyStatement(
                effect=iam.Effect.ALLOW,
                principals=[iam.AnyPrincipal()],
                actions=["s3:GetObject"],
                resources=[f"{bucket.bucket_arn}/*"]
            )
        )

        # Add explicit versioning
        bucket.versioned = True

        # Add explicit lifecycle rules
        bucket.lifecycle_rules = [
            s3.LifecycleRule(
                enabled=True,
                status=s3.LifecycleRuleStatus.INCLUDE,
                expiration=cdk.Duration.days(30),
                noncurrent_version_expiration=cdk.Duration.days(60)
            )
        ]

        # Add explicit default object lock
        bucket.default_encryption_key = s3.BucketEncryption.S3_MANAGED
        bucket.default_versioned = True
        bucket.default_encryption = s3.BucketEncryption.S3_MANAGED
        bucket.default_version_retention = cdk.Duration.days(30)
        bucket.default_encryption_key_rotation = cdk.Duration.days(365)

        # Add explicit logging
        bucket.add_to_resource_policy(
            iam.PolicyStatement(
                effect=iam.Effect.ALLOW,
                principals=[iam.AnyPrincipal()],
                actions=["s3:PutObject"],
                resources=[f"{bucket.bucket_arn}/*"],
                conditions={
                    "StringLike": {
                        "s3:x-amz-acl": ["bucket-owner-full-control"]
                    }
                }
            )
        )

        # Add explicit access logging
        bucket.add_event_notification(
            s3.EventType.OBJECT_CREATED_PUT,
            s3.NotificationConfig(
                target=s3deploy.B