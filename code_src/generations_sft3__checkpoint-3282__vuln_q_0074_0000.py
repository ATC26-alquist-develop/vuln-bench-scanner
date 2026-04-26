from aws_cdk import core as cdk
from aws_cdk.aws_s3 import Bucket, BucketEncryption, EncryptionOption
from aws_cdk.aws_kms import Key, KeyPolicy, Statement

class SecureS3Stack(cdk.Stack):

    def __init__(self, app: cdk.App, id: str, **kwargs) -> None:
        super().__init__(app, id, **kwargs)

        # Create a secure S3 bucket with encryption
        self.bucket = Bucket(
            self,
            "SecureBucket",
            encryption=BucketEncryption.KMS,
            encryption_option=EncryptionOption.BUCKET_ENCRYPTION,
            removal_policy=cdk.RemovalPolicy.DESTROY  # Secure deletion on stack removal
        )

        # Grant necessary permissions
        self.bucket.grant_read_write(
            self.bucket,
            Statement(
                principals=[cdk.ArnPrincipal(f"arn:aws:iam::{cdk.ArnPrincipal.account_id}:root")],
                actions=["s3:*"],
                resources=[self.bucket.bucket_arn, f"{self.bucket.bucket_arn}/*"]
            )
        )