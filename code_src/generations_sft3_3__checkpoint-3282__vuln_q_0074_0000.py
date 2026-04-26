from aws_cdk import core as cdk
from aws_cdk.aws_s3 import Bucket, BucketEncryption
from aws_cdk.aws_kms import Key

class SecureS3Stack(cdk.Stack):

    def __init__(self, app: cdk.App, id: str, **kwargs) -> None:
        super().__init__(app, id, **kwargs)

        # Create a secure KMS key for encryption
        self.kms_key = Key(self, "SecureKMSKey",
            description="Secure S3 bucket encryption key",
            enable_key_rotation=True
        )

        # Create S3 bucket with encryption
        self.bucket = Bucket(self, "SecureBucket",
            bucket_name=f"secure-bucket-{cdk.RandomString()}",
            encryption=BucketEncryption.KMS,
            encryption_key=self.kms_key,
            removal_policy=cdk.RemovalPolicy.DESTROY  # Secure deletion on stack removal
        )