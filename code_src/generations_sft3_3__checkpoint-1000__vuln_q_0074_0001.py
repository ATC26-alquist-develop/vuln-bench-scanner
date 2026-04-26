```python
from aws_cdk import (
    core,
    aws_s3 as s3,
    aws_kms as kms,
    aws_s3_deployment as s3deploy,
    aws_s3_deployment_props as s3deploy_props,
    aws_s3_bucket as bucket,
    aws_s3_bucket_props as bucket_props,
    aws_s3_deployment as s3deploy,
    aws_s3_deployment_props as s3deploy_props
)

class SecureS3BucketStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Create a KMS key for encryption
        key = kms.Key(self, "SecureS3Key",
            enable_key_rotation=True,
            description="Key for encrypting S3 bucket contents"
        )

        # Create an S3 bucket with encryption enabled
        bucket = s3.Bucket(self, "SecureS3Bucket",
            bucket_name="secure-s3-bucket",
            encryption=s3.BucketEncryption.KMS,
            encryption_key=key,
            block_public_access=s3.BlockPublicAccess.BLOCK_ALL,
            versioned=True,
            removal_policy=core.RemovalPolicy.DESTROY
        )

        # Deploy files to the bucket
        s3deploy.BucketDeployment(self, "DeployFiles",
            sources=[s3deploy.Source.asset("./sensitive_data")],
            destination_bucket=bucket,
            distribution=None,
            distribution_www_domain=None,
            prune=True
        )

        # Add a policy to allow only specific IAM roles to access the bucket
        bucket.add_to_resource_policy(
            core.PolicyStatement(
                actions=["s3:GetObject"],
                resources=[f"{bucket.bucket_arn}/*"],
                principals=[core.ServicePrincipal("service-role/AWSLambdaBasicExecutionRole")]
            )
        )

        # Add a policy to allow only specific IAM roles to access the bucket
        bucket.add_to_resource_policy(
            core.PolicyStatement(
                actions=["s3:PutObject"],
                resources=[f"{bucket.bucket_arn}/*"],
                principals=[core.ServicePrincipal("service-role/AWSLambdaBasicExecutionRole")]
            )
        )

        # Add a policy to allow only specific IAM roles to access the bucket
        bucket.add_to_resource_policy(
            core.PolicyStatement(
                actions=["s3:DeleteObject"],
                resources=[f"{bucket.bucket_arn}/*"],
                principals=[core.ServicePrincipal("service-role/AWSLambdaBasicExecutionRole")]
            )
        )

        # Add a policy to allow only specific IAM roles to access the bucket
        bucket.add_to_resource_policy(
            core.PolicyStatement(
                actions=["s3:ListBucket"],
                resources=[bucket.bucket_arn],
                principals=[core.ServicePrincipal("service-role/AWSLambdaBasicExecutionRole")]
            )
        )

        # Add a policy to allow only specific IAM roles to access the bucket
        bucket.add_to_resource_policy(
            core.PolicyStatement(
                actions=["s3:PutObjectAcl"],
                resources=[f"{bucket.bucket_arn}/*"],
                principals=[core.ServicePrincipal("service-role/AWSLambdaBasicExecutionRole")]
            )
        )

        # Add a policy to allow only specific IAM roles to access the bucket
        bucket.add_to_resource_policy(
            core.PolicyStatement(
                actions=["s3:GetObjectAcl"],
                resources=[f"{bucket.bucket_arn}/*"],
                principals=[core.ServicePrincipal("service-role/AWSLambdaBasicExecutionRole")]
            )
        )

        # Add a policy to allow only specific IAM roles to access the bucket
        bucket.add_to_resource_policy(
            core.PolicyStatement(
                actions=["s3:PutBucketPolicy"],
                resources=[bucket.bucket_arn],
                principals=[core.ServicePrincipal("service-role/AWSLambda