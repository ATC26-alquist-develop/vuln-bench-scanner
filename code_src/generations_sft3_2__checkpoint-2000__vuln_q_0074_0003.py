from aws_cdk import (
    core,
    aws_kms as _kms,
    aws_s3 as _s3,
    aws_s3_deployment as _s3deploy,
    aws_s3_assets as _assets
)
from constructs import Construct

class SecureS3DeploymentStack(core.Stack):

    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Create a secure KMS key with proper key policies
        self.kms_key = _kms.Key(
            self, "SecureKMSKey",
            enable_key_rotation=True,
            description="Secure S3 bucket encryption key",
            encryption_key_policies={
                "AWS_KMS_Default_Encryption_Criterion": {
                    "EncryptionCriteria": {
                        "Algorithm": "AES_256"
                    }
                }
            }
        )

        # Create a secure S3 bucket with server-side encryption
        self.bucket = _s3.Bucket(
            self, "SecureBucket",
            bucket_name=f"secure-bucket-{self.region}-{self.account}",
            encryption=_s3.BucketEncryption.KMS,
            encryption_key=self.kms_key,
            server_side_encryption_configuration=[
                _s3.BucketServerSideEncryptionConfiguration(
                    rule=_s3.BucketServerSideEncryptionRule(
                        enabled=True,
                        protocol=_s3.BucketServerSideEncryptionRuleProtocol(
                            all_=True
                        ),
                        storage_class=_s3.BucketServerSideEncryptionRuleStorageClass(
                            ALL
                        )
                    )
                )
            ]
        )

        # Securely deploy assets to S3
        with _assets.Asset(self, "SecureAssets") as asset:
            # Use a secure path for deployment
            _s3deploy.BucketDeployment(
                self, "DeployAssets",
                sources=[_s3deploy.Source.asset(asset.path)],
                destination_bucket=self.bucket
            )