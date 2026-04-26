from aws_cdk import (
    core as cdk,
    aws_s3 as s3,
    aws_s3_deployment as s3deploy,
    aws_kms as kms,
    aws_secretsmanager as secretsmanager,
    Stack
)

class SecureS3Stack(Stack):

    def __init__(self, app: core.App, id: str, **kwargs) -> None:
        super().__init__(app, id, **kwargs)

        # Create a secure bucket with encryption
        bucket = s3.Bucket(
            self,
            "SecureBucket",
            bucket_name=f"secure-bucket-{cdk.RandomName.next()}",
            encryption=s3.BucketEncryption.KMS,
            encryption_key=kms.Key(self, "EncryptionKey", description="Secure S3 Bucket Encryption")
        )

        # Deploy objects with encryption
        with open("example.txt", "w") as f:
            f.write("Sensitive data")
        
        s3deploy.BucketDeployment(
            self,
            "DeployObjects",
            sources=[s3deploy.Source.file("example.txt")],
            destination_bucket=bucket
        )

        # Add versioning
        bucket.versioning_enabled = True

        # Add logging
        bucket.logging_enabled = s3.LoggingConfig(
            log_bucket=bucket,
            log_object_key_prefix="logs/"
        )

        # Add default CORS configuration
        bucket.add_cors_rule(
            allowed_methods=[s3.CorsRule.http_get=True],
            allowed_origins=["*"],
            max_age_seconds=300
        )