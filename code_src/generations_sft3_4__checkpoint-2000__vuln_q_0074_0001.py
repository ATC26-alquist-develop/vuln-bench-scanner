from aws_cdk import (
    core,
    aws_s3 as s3,
    aws_kms as kms,
    aws_s3_deployment as s3deploy,
    aws_s3_bucket_public_access as bucket_public_access
)

class SecureS3BucketStack(core.Stack):

    def __init__(self, app: core.App, id: str, **kwargs) -> None:
        super().__init__(app, id, **kwargs)

        # Create a KMS key for encryption
        key = kms.Key(self, "SecureKey",
            enable_at_provision_time=True,
            description="Secure key for encrypting S3 bucket contents"
        )

        # Create an S3 bucket with encryption enabled
        bucket = s3.Bucket(self, "SecureBucket",
            bucket_name=f"secure-data-{self.region}-{self.account}",
            encryption_key=key,
            block_public_access=bucket_public_access.BlockPublicAccess.BLOCK_ALL
        )

        # Deploy objects to the bucket
        s3deploy.BucketDeployment(self, "DeployObjects",
            sources=[s3deploy.Source.tree("./sensitive_data", "Sensitive Data")],
            destination_bucket=bucket
        )

        # Add logging
        core.CfnOutput(self, "BucketName", value=bucket.bucket_name)
        core.CfnOutput(self, "EncryptionKeyArn", value=key.key_arn)