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
            versioned=True,
            auto_delete_objects=cdk.Duration.days(7)
        )

        # Add KMS key for encryption (if needed)
        self.encryption_key = Key(
            self,
            "EncryptionKey",
            enabled=True,
            description="Secure S3 bucket encryption key",
            encryption_option=KeyEncryptionOption.LEGACY_KEY encryption_option=KeyEncryptionOption.AWS_KMS
        )

        # Attach policy to allow KMS key usage
        self.encryption_key.add_to_resource_policy(
            Statement(
                effect=cdk.Effect.ALLOW,
                principals=[cdk.ServicePrincipal("s3.amazonaws.com")],
                actions=["kms:Encrypt", "kms:Decrypt", "kms:ReEncrypt*"],
                resources=["*"]
            )
        )

        # Add tags for audit and management
        self.bucket.add_tags(
            "Environment", "Production",
            "Owner", "AWS CDK",
            "Team", "DevOps"
        )