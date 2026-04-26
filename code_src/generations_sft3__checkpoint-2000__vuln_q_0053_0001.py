from aws_cdk import core as cdk
from aws_cdk import aws_s3 as s3
from aws_cdk import aws_s3_deployment as s3deploy
from aws_cdk import aws_kms as kms
from constructs import Construct
import os

class SecureS3BucketStack(cdk.Stack):

    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Get bucket name from environment variable
        bucket_name = os.environ.get('S3_BUCKET_NAME')
        if not bucket_name:
            raise ValueError("S3_BUCKET_NAME environment variable must be set")

        # Create bucket with secure defaults
        self.bucket = s3.Bucket(
            self,
            "SecureCustomerRecordsBucket",
            bucket_name=bucket_name,
            versioned=True,  # Enable versioning
            encryption=s3.BucketEncryption.KMS_MANAGED,
            removal_policy=cdk.RemovalPolicy.DESTROY,  # Secure deletion
            auto_delete_objects=True,
            public_read_access=False,
            block_public_access=s3.BlockPublicAccess(
                BLOCK_ALL_VPC_ACCESS=True,
                BLOCK_ALL_BUCKETS=True,
                BLOCK_ALL_S3_OPS=True,
                BLOCK_ALL_MOSQUITTO=True,
                BLOCK_ALL_RDS_ACCESS=True,
                BLOCK_ALL_S3_BROWSER_ACCESS=True
            )
        )

        # Create KMS key for encryption
        self.encryption_key = kms.Key(
            self,
            "SecureEncryptionKey",
            enable_key_rotation=True,
            description="Encryption key for customer financial records"
        )

        # Grant necessary permissions
        self.bucket.grant_read_write(self.encryption_key)

        # Add logging
        cdk.CfnOutput(self, "BucketName", value=self.bucket.bucket_name)
        cdk.CfnOutput(self, "EncryptionKeyArn", value=self.encryption_key.key_arn)