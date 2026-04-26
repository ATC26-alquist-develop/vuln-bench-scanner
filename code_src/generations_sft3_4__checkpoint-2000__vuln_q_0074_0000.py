from aws_cdk import core as cdk
from aws_cdk import aws_s3 as s3
from aws_cdk import aws_s3_deployment as s3deploy
from aws_cdk import aws_kms as kms
from constructs import Construct

class SecureS3BucketStack(cdk.Stack):

    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Create a secure bucket with encryption
        bucket = s3.Bucket(
            self,
            "SecureBucket",
            bucket_name=f"secure-bucket-{cdk.Aws.RandomValueGenerator.generate().string(8)}",
            encryption=s3.BucketEncryption.KMS,
            encryption_key=kms.Key(self, "EncryptionKey", description="Secure S3 Bucket Encryption")
        )

        # Securely deploy objects to the bucket
        s3deploy.BucketDeployment(
            self,
            "SecureDeployment",
            sources=[s3deploy.Source.asset("./static-content")],
            destination_bucket=bucket
        )

        # Add versioning
        bucket.versioned = True

        # Add logging
        bucket.logging = s3.BucketLoggingConfig(
            logging_config=s3.BucketLoggingConfigProperty(
                enabled=True,
                target_bucket=bucket,
                target_key="s3-logs"
            )
        )

        # Add default CORS configuration
        bucket.cors = [
            s3.BucketCorsConfiguration(
                rules=[
                    s3.BucketCorsRule(
                        allowed_headers=["*"],
                        allowed_methods=[s3.HttpMethod.GET, s3.HttpMethod.PUT],
                        allowed_origins=["*"],
                        max_age_seconds=3000
                    )
                ]
            )
        ]