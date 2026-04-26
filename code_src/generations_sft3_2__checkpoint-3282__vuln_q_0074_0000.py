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
            bucket_name=f"secure-bucket-{cdk.ArnGenerator.generate_id_for_stack(self)}",
            encryption=BucketEncryption.KMS_MANAGED,
            removal_policy=cdk.RemovalPolicy.DESTROY,  # Secure deletion
            auto_delete_objects=True,  # Enable auto-deletion
            versioned=True,  # Enable object versioning
            block_public_access=cdk.BlockPublicAccess.BLOCK_ALL,
            public_read_access=False,
            website_index_document="index.html",
            website_error_document="error.html"
        )

        # Add KMS key for encryption (if needed)
        self.encryption_key = Key(
            self,
            "EncryptionKey",
            enable_key_rotation=True,
            admin_group=["system:maintenance"]
        )