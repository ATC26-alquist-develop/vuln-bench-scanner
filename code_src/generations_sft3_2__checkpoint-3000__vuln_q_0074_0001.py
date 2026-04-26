from aws_cdk import (
    core,
    aws_s3 as s3,
    aws_kms as kms,
    aws_s3_deployment as s3deploy
)

class SecureS3BucketStack(core.Stack):
    def __init__(self, app: core.App, id: str, **kwargs) -> None:
        super().__init__(app, id, **kwargs)

        # Create a KMS key for encryption
        key = kms.Key(self, "SecureKey", 
            key_id="alias/secure-key",
            description="Secure key for S3 bucket encryption",
            enabled=True,
            enable_key_rotation=True
        )

        # Create an S3 bucket with encryption enabled
        bucket = s3.Bucket(self, "SecureBucket",
            bucket_name=f"secure-data-{core.Stack.of(self).region}-{core.Stack.of(self).account}",
            encryption_key=key,
            block_public_access=s3.BlockPublicAccess.BLOCK_ALL,
            removal_policy=core.RemovalPolicy.DESTROY
        )

        # Deploy objects to the bucket
        s3deploy.BucketDeployment(self, "DeployObjects",
            sources=[s3deploy.Source.tree("./", "index.html")],
            destination_bucket=bucket
        )