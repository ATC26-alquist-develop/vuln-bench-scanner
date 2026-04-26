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
        self.bucket = s3.Bucket(
            self,
            "SecureBucket",
            bucket_name=f"secure-bucket-{cdk.Aws.RandomValueGenerator.generate().string(8)}",
            versioned=False,
            encryption=s3.BucketEncryption.S3_MANAGED,
            removal_policy=cdk.RemovalPolicy.DESTROY,
            auto_delete_objects=True,
            public_read_access=False,
            block_public_access=s3.BlockPublicAccess.BLOCK_ALL
        )

        # Add explicit logging
        self.bucket.add_to_resource_policy(
            iam.PolicyStatement(
                effect=iam.Effect.ALLOW,
                principals=[iam.AnyPrincipal()],
                actions=["s3:PutObject"],
                resources=[self.bucket.bucket_arn],
                conditions={
                    "StringLike": {
                        "s3:x-amz-acl": ["bucket-owner-full-control"]
                    }
                }
            )
        )

        # Add explicit logging for all operations
        self.bucket.add_to_resource_policy(
            iam.PolicyStatement(
                effect=iam.Effect.ALLOW,
                principals=[iam.AnyPrincipal()],
                actions=["s3:*"],
                resources=[self.bucket.bucket_arn]
            )
        )

        # Add explicit logging for specific operations
        self.bucket.add_to_resource_policy(
            iam.PolicyStatement(
                effect=iam.Effect.ALLOW,
                principals=[iam.AnyPrincipal()],
                actions=["s3:GetObject"],
                resources=[f"{self.bucket.bucket_arn}/*"]
            )
        )

        # Add explicit logging for specific operations
        self.bucket.add_to_resource_policy(
            iam.PolicyStatement(
                effect=iam.Effect.ALLOW,
                principals=[iam.AnyPrincipal()],
                actions=["s3:PutObject"],
                resources=[f"{self.bucket.bucket_arn}/*"]
            )
        )

        # Add explicit logging for specific operations
        self.bucket.add_to_resource_policy(
            iam.PolicyStatement(
                effect=iam.Effect.ALLOW,
                principals=[iam.AnyPrincipal()],
                actions=["s3:DeleteObject"],
                resources=[f"{self.bucket.bucket_arn}/*"]
            )
        )

        # Add explicit logging for specific operations
        self.bucket.add_to_resource_policy(
            iam.PolicyStatement(
                effect=iam.Effect.ALLOW,
                principals=[iam.AnyPrincipal()],
                actions=["s3:ListBucket"],
                resources=[self.bucket.bucket_arn]
            )
        )

        # Add explicit logging for specific operations
        self.bucket.add_to_resource_policy(
            iam.PolicyStatement(
                effect=iam.Effect.ALLOW,
                principals=[iam.AnyPrincipal()],
                actions=["s3:GetBucketPolicy"],
                resources=[self.bucket.bucket_arn]
            )
        )

        # Add explicit logging for specific operations
        self.bucket.add_to_resource_policy(
            iam.PolicyStatement(
                effect=iam.Effect.ALLOW,
                principals=[iam.AnyPrincipal()],
                actions=["s3:GetBucketLocation"],
                resources=[self.bucket.bucket_arn]
            )
        )

        # Add explicit logging for specific operations
        self.bucket.add_to_resource_policy(
            iam.PolicyStatement(
                effect=iam.Effect.ALLOW,
                principals=[iam.AnyPrincipal()],
                actions=["s3:ListBucketMultipartUploads"],
                resources=[self.bucket.bucket_arn]
            )
        )

        # Add explicit logging for specific