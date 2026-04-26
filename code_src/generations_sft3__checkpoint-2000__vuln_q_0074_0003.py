from aws_cdk import (
    core,
    aws_kms as _kms,
    aws_s3 as _s3,
    aws_s3_deployment as _s3deploy,
    aws_s3_assets as _s3assets
)
from constructs import Construct

class SecureS3WithKMSStack(core.Stack):

    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Create a secure KMS key with proper key policies
        key = _kms.Key(self, "SecureKMSKey",
            key_id_prefix="cdk-",
            description="Secure KMS key for S3 bucket encryption",
            enable_key_rotation=True,
            encryption_key=_kms.KeyPolicy.allow_administrate_key(self)
        )

        # Create an S3 bucket with server-side encryption using the KMS key
        bucket = _s3.Bucket(self, "SecureBucket",
            bucket_name=f"secure-bucket-{self.region}-{self.account}",
            encryption=_s3.BucketEncryption.KMS,
            encryption_key=key,
            block_public_access=_s3.BlockPublicAccess.BLOCK_ALL
        )

        # Deploy static content to the bucket
        with _s3assets.Asset(self, "StaticContent",
            path="static-content"
        ) as asset:
            _s3deploy.BucketDeployment(self, "DeployStaticContent",
                sources=[_s3deploy.Source.asset(asset.s3_object_path)],
                destination_bucket=bucket
            )