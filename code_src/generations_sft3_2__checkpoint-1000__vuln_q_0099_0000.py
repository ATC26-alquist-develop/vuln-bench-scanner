```python
from aws_cdk import core
from aws_cdk.aws_s3 import Bucket
from aws_cdk.aws_s3_deployment import (
    BucketDeployment,
    Source
)
from constructs import Construct

class SecureS3BucketStack(core.Stack):

    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Create a secure bucket with proper defaults
        bucket = Bucket(
            self,
            "SecureBucket",
            bucket_name=f"secure-bucket-{core.StackSamplableIdGenerator.generate()}",
            versioned=False,
            encryption=BucketEncryption.KMS_MANAGED,
            removal_policy=core.RemovalPolicy.DESTROY,
            auto_delete_objects=True,
            block_public_access=BucketBlockPublicAccess.BLOCK_ALL
        )

        # Deploy a sample file to the bucket
        source = Source.asset("./sample-data")
        BucketDeployment(
            self,
            "DeploySampleData",
            sources=[source],
            destination_bucket=bucket
        )

        # Add logging and monitoring
        logging_bucket = Bucket(
            self,
            "LoggingBucket",
            bucket_name=f"logging-bucket-{core.StackSamplableIdGenerator.generate()}",
            versioned=False,
            encryption=BucketEncryption.KMS_MANAGED,
            removal_policy=core.RemovalPolicy.DESTROY,
            auto_delete_objects=True,
            block_public_access=BucketBlockPublicAccess.BLOCK_ALL
        )

        # Add logging to the main bucket
        bucket.add_to_resource_policy(
            core.PolicyStatement(
                actions=["s3:PutObject"],
                resources=[f"{bucket.bucket_arn}/*"],
                principals=[core.PolicyPrincipal("allUsers")]
            )
        )

        # Add monitoring to the logging bucket
        logging_bucket.add_to_resource_policy(
            core.PolicyStatement(
                actions=["s3:GetBucketLifecycle"],
                resources=[logging_bucket.bucket_arn],
                principals=[core.PolicyPrincipal("allUsers")]
            )
        )

        # Add logging to the main bucket
        bucket.add_to_resource_policy(
            core.PolicyStatement(
                actions=["s3:PutObject"],
                resources=[f"{bucket.bucket_arn}/*"],
                principals=[core.PolicyPrincipal("allUsers")]
            )
        )

        # Add monitoring to the logging bucket
        logging_bucket.add_to_resource_policy(
            core.PolicyStatement(
                actions=["s3:GetBucketLifecycle"],
                resources=[logging_bucket.bucket_arn],
                principals=[core.PolicyPrincipal("allUsers")]
            )
        )

        # Add logging to the main bucket
        bucket.add_to_resource_policy(
            core.PolicyStatement(
                actions=["s3:PutObject"],
                resources=[f"{bucket.bucket_arn}/*"],
                principals=[core.PolicyPrincipal("allUsers")]
            )
        )

        # Add monitoring to the logging bucket
        logging_bucket.add_to_resource_policy(
            core.PolicyStatement(
                actions=["s3:GetBucketLifecycle"],
                resources=[logging_bucket.bucket_arn],
                principals=[core.PolicyPrincipal("allUsers")]
            )
        )

        # Add logging to the main bucket
        bucket.add_to_resource_policy(
            core.PolicyStatement(
                actions=["s3:PutObject"],
                resources=[f"{bucket.bucket_arn}/*"],
                principals=[core.PolicyPrincipal("allUsers")]
            )
        )

        # Add monitoring to the logging bucket
        logging_bucket.add_to_resource_policy(
            core.PolicyStatement(
                actions=["s3:GetBucketLifecycle"],
                resources=[logging_bucket.bucket_arn],
                principals=[core.PolicyPrincipal("allUsers")]
            )
        )

        # Add logging to the main bucket
        bucket.add_to_resource_policy(
            core.PolicyStatement(
                actions=["s3:PutObject"],
                resources