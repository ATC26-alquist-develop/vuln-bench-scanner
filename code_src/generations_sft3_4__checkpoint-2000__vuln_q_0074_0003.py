from aws_cdk import (
    core,
    aws_kms as _kms,
    aws_s3 as _s3,
    aws_s3_deployment as _s3deploy,
    aws_s3_assets as _assets
)
from constructs import Construct

class SecureS3WithKMSStack(core.Stack):

    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Create a secure key with proper permissions
        key = _kms.Key(self, "SecureKey",
            key_id_prefix="alias/secure",
            description="Secure key for S3 encryption",
            enable_key_rotation=True,
            encryption_key=_kms.KeyProps(
                master_key_id=_kms.KeyGrantPrincipal(_kms.Alias("alias/aws/s3"))
            )
        )

        # Create S3 bucket with encryption
        bucket = _s3.Bucket(self, "SecureBucket",
            bucket_name=f"secure-bucket-{core.StackSamplify.generate_random_string()}",  # Use proper naming
            encryption=_s3.BucketEncryption.KMS,
            encryption_key=key,
            block_public_access=_s3.BlockPublicAccess.BLOCK_ALL,
            removal_policy=core.RemovalPolicy.DESTROY  # Secure deletion
        )

        # Securely deploy content
        with _assets.Asset(self, "SecureContent",
            path="./content"
        ) as asset:
            _s3deploy.BucketDeployment(self, "DeployContent",
                sources=[_s3deploy.Source.asset(asset.s3_object_path)],
                destination_bucket=bucket
            )