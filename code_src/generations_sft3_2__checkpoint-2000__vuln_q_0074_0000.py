from aws_cdk import core as cdk
from aws_cdk.aws_s3 import Bucket, BucketEncryption
from aws_cdk.aws_kms import Key
from aws_cdk import aws_kms as _kms

class SecureS3Stack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Create a key for encryption
        key = Key(self, "SecureKey",
                  description="Secure S3 bucket encryption key",
                  enable_key_rotation=True)

        # Create S3 bucket with encryption
        bucket = Bucket(self, "SecureBucket",
                       bucket_name=f"secure-bucket-{cdk.Aws.RandomValueGenerator.generate().string()},
                       encryption=BucketEncryption.KMS,
                       encryption_key=key,
                       removal_policy=cdk.RemovalPolicy.DESTROY)

        # Add any additional security configurations here
        # For example, enable server access logging
        bucket.add_server_access_log("secure-bucket-logs")