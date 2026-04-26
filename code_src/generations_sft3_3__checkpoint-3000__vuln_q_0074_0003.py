from aws_cdk import (
    core as cdk,
    s3 as s3,
    kms as kms,
    Duration
)
from constructs import Construct

class SecureS3WithKMSStack(cdk.Stack):

    def __init__(self, scope: Construct, id: str, *, bucket_name: str, kms_key_arn: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Validate inputs
        core.CfnCondition(self, 'ValidBucketName',
            expression=f'is-valid-bucket-name-{bucket_name}'
        )

        # Create bucket with secure defaults
        bucket = s3.Bucket(self, "SecureBucket",
            bucket_name=bucket_name,
            encryption=s3.BucketEncryption.KMS,
            encryption_key=kms.Key.from_arn(self, "KMSKey", 
                key_arn=kms_key_arn
            ),
            versioned=True,
            removal_policy=cdk.RemovalPolicy.DESTROY
        )

        # Add additional security configurations
        bucket.add_to_resource_policy(
            cdk.CfnPermission(self, "BucketPolicy",
                principal=cdk.CfnPrincipal("arn:aws:iam::aws:all-users"),
                action=["s3:GetObject"],
                effect=cdk.CfnPermission.Effect.DENY,
                resource=bucket.bucket_arn,
                condition=cdk.CfnCondition("DenyGetObject")
            )
        )

        # Configure logging
        bucket.logging_enabled = s3.BucketLoggingEnabled(
            logging_configuration=s3.LogObjectConfiguration(
                log_file_prefix="secure-logs/",
                destination_bucket=bucket
            )
        )

        # Apply condition for logging
        core.CfnOutput(self, "SecureLogsBucket",
            value=bucket.bucket_name,
            export_name=f"{self.stack_name}-SecureLogsBucket"
        )