from aws_cdk import (
    core as cdk,
    s3 as s3stack,
    kms as kms,
    aws_s3 as s3,
    aws_kms as kms,
    aws_s3_deployment as s3deploy
)
from constructs import Construct

class SecureS3DeploymentStack(cdk.Stack):

    def __init__(self, scope: Construct, id: str, *, kms_key: kms.Key, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Create a secure S3 bucket
        bucket = s3.Bucket(self, "SecureBucket",
            encryption=s3.BucketEncryption.KMS,
            encryption_key=kms_key,
            block_public_access=s3.BlockPublicAccess.BLOCK_ALL
        )

        # Securely deploy objects to the bucket
        s3deploy.BucketDeployment(self, "DeployWebsite",
            sources=[s3deploy.Source.asset("./website")],
            destination_buckets=[bucket]
        )