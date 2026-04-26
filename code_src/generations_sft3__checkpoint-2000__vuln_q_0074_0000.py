from aws_cdk import core as cdk
from aws_cdk.aws_s3 import Bucket, BucketEncryption
from aws_cdk.aws_kms import Key
from aws_cdk import aws_kms as _kms

class SecureS3Stack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Create a key for encryption
        self.encryption_key = Key(self, "SecureKey",
            description="Secure S3 Bucket Encryption Key",
            enable_key_rotation=True
        )

        # Create encrypted bucket with default encryption
        self.bucket = Bucket(self, "SecureBucket",
            encryption=BucketEncryption.KMS,
            encryption_key=self.encryption_key,
            versioned=True,
            removal_policy=cdk.RemovalPolicy.DESTROY
        )