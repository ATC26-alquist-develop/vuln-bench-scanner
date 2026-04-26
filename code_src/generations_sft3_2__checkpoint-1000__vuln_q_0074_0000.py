from aws_cdk import core
from aws_cdk.aws_s3 import Bucket, BucketEncryption
from aws_cdk.aws_kms import Key
from aws_cdk import aws_kms as _kms

class SecureS3BucketStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Create a KMS key for encryption
        self.encryption_key = Key(self, "SecureEncryptionKey",
                                 description="Secure S3 bucket encryption key",
                                 enable_key_rotation=True)

        # Create S3 bucket with encryption
        self.bucket = Bucket(self, "SecureBucket",
                             bucket_name=f"secure-bucket-{self.region}-{self.account}",
                             encryption=BucketEncryption.KMS,
                             encryption_key=self.encryption_key,
                             removal_policy=core.RemovalPolicy.DESTROY,
                             auto_delete_objects=True)

        # Add some basic logging
        core.CfnOutput(self, "BucketName", value=self.bucket.bucket_name)
        core.CfnOutput(self, "EncryptionKeyArn", value=self.encryption_key.key_arn)