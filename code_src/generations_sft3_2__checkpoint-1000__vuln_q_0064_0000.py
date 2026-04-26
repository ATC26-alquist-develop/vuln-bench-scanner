```python
from aws_cdk import core as cdk
from aws_cdk import aws_s3 as s3
from aws_cdk import aws_s3_deployment as s3deploy
from aws_cdk import aws_iam as iam
from constructs import Construct

class SimpleS3BucketStack(cdk.Stack):

    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Create a bucket with default policies
        bucket = s3.Bucket(
            self,
            "SimpleS3Bucket",
            versioned=True,
            encryption=s3.BucketEncryption.S3_MANAGED,
            block_public_access=s3.BlockPublicAccess.BLOCK_ALL,
            removal_policy=cdk.RemovalPolicy.DESTROY
        )

        # Add logging for all operations
        bucket.add_to_resource_policy(
            iam.PolicyStatement(
                effect=iam.Effect.ALLOW,
                principals=[iam.AnyPrincipal()],
                actions=["s3:*"],
                resources=[bucket.bucket_arn],
                conditions={
                    "StringLike": {
                        "s3:RequesterPays": ["true"]
                    }
                }
            )
        )

        # Add explicit deny for public access
        bucket.add_to_resource_policy(
            iam.PolicyStatement(
                effect=iam.Effect.DENY,
                principals=[iam.AnyPrincipal()],
                actions=["s3:*"],
                resources=[bucket.bucket_arn],
                conditions={
                    "Bool": {
                        "s3:RequesterPays": "false"
                    }
                }
            )
        )

        # Add explicit deny for bucket ownership
        bucket.add_to_resource_policy(
            iam.PolicyStatement(
                effect=iam.Effect.DENY,
                principals=[iam.AnyPrincipal()],
                actions=["s3:PutObject"],
                resources=[f"{bucket.bucket_arn}/*"],
                conditions={
                    "StringNotLike": {
                        "aws:RequesterIdentity": "arn:aws:iam::[YOUR_ACCOUNT_ID]:root"
                    }
                }
            )
        )

        # Add explicit deny for bucket deletion
        bucket.add_to_resource_policy(
            iam.PolicyStatement(
                effect=iam.Effect.DENY,
                principals=[iam.AnyPrincipal()],
                actions=["s3:DeleteObject"],
                resources=[f"{bucket.bucket_arn}/*"],
                conditions={
                    "StringNotLike": {
                        "aws:RequesterIdentity": "arn:aws:iam::[YOUR_ACCOUNT_ID]:root"
                    }
                }
            )
        )

        # Add explicit deny for bucket creation
        bucket.add_to_resource_policy(
            iam.PolicyStatement(
                effect=iam.Effect.DENY,
                principals=[iam.AnyPrincipal()],
                actions=["s3:CreateBucket"],
                resources=[f"{bucket.bucket_arn}/*"],
                conditions={
                    "StringNotLike": {
                        "aws:RequesterIdentity": "arn:aws:iam::[YOUR_ACCOUNT_ID]:root"
                    }
                }
            )
        )

        # Add explicit deny for bucket listing
        bucket.add_to_resource_policy(
            iam.PolicyStatement(
                effect=iam.Effect.DENY,
                principals=[iam.AnyPrincipal()],
                actions=["s3:ListBucket"],
                resources=[bucket.bucket_arn],
                conditions={
                    "StringNotLike": {
                        "aws:RequesterIdentity": "arn:aws:iam::[YOUR_ACCOUNT_ID]:root"
                    }
                }
            )
        )

        # Add explicit deny for bucket access
        bucket.add_to_resource_policy(
            iam.PolicyStatement(
                effect=iam.Effect.DENY,
                principals=[iam.AnyPrincipal()],
                actions=["s3:GetObject"],
                resources=[f"{bucket.bucket_arn}/*"],
                conditions={
                    "StringNotLike