from aws_cdk import core as cdk
from aws_cdk.aws_s3 import Bucket, BucketEncryption
from aws_cdk.aws_kms import Key, KeyPolicy, AllowedPrincipal

class SecureS3Stack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Create a secure S3 bucket with encryption
        self.bucket = Bucket(
            self,
            "SecureBucket",
            bucket_name=f"secure-bucket-{cdk.ArnGenerator.generate_id_for_resource()}",
            encryption=BucketEncryption.KMS_MANAGED,
            removal_policy=cdk.RemovalPolicy.DESTROY,  # Secure deletion
            versioned=True,
            auto_delete_objects=cdk.Duration.days(30)  # Enable auto-deletion
        )

        # Add KMS key for encryption
        self.encryption_key = Key(
            self,
            "EncryptionKey",
            description="Secure S3 bucket encryption key",
            enable_key_rotation=True
        )

        # Set up proper access controls
        self.encryption_key.grant_read_write(
            self.bucket
        )

        # Add policy to allow only specific principals
        self.encryption_key.grant_principal(
            AllowedPrincipal(self.bucket)
        ).add_to_principals_policy(
            cdk.aws_iam.PolicyStatement(
                effect=cdk.aws_iam.Effect.ALLOW,
                actions=["kms:Encrypt", "kms:Decrypt"],
                resources=["*"]
            )
        )

        # Add logging
        logging_bucket = self.bucket.add_versioned_object_store_logging(
            "ObjectLogging",
            destination=self.bucket,
            prefix="logs/"
        )

        # Add versioning
        self.bucket.add_versioning()

        # Add default cors
        self.bucket.add_cors_rule(
            allowed_methods=[cdk.aws_s3.CorsHttpMethod.GET],
            max_age_seconds=300,
            allowed_origins=["*"]
        )