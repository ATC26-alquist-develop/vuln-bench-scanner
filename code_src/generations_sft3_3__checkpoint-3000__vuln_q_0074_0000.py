from aws_cdk import (
    core as cdk,
    aws_s3 as s3,
    aws_s3_deployment as deployment,
    aws_kms as kms,
    aws_secretsmanager as secretsmanager,
    Stack
)

class S3EncryptionStack(cdk.Stack):

    def __init__(self, app: core.App, id: str, **kwargs) -> None:
        super().__init__(app, id, **kwargs)

        # Create a secure KMS key for encryption
        key = kms.Key(self, "SecureKey",
            enable_at_creation=True,
            description="Secure S3 bucket encryption key",
            encryption_context={"Environment": self.region}
        )

        # Create S3 bucket with encryption
        bucket = s3.Bucket(self, "SecureBucket",
            bucket_name=f"secure-bucket-{cdk.ArnGenerator.generate_hash()}",
            encryption_key=key,
            versioned=True,
            removal_policy=cdk.RemovalPolicy.DESTROY  # Secure deletion
        )

        # Deploy contents with encryption
        deployment.BucketDeployment(self, "DeployContent",
            sources=[deployment.Source.tree("./content", "content")],
            destination=bucket,
            encryption_key=key
        )

        # Add logging
        core.CfnOutput(self, "BucketARN", value=bucket.bucket_arn)
        core.CfnOutput(self, "EncryptionKeyARN", value=key.key_arn)