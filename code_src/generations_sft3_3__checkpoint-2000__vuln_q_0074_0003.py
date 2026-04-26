from aws_cdk import (
    core,
    s3,
    kms,
    CfnOutput
)
from constructs import Construct

class SecureS3WithKMSStack(core.Stack):

    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Create S3 bucket with server-side encryption using KMS key
        bucket = s3.Bucket(
            self,
            "SecureBucket",
            encryption=s3.BucketEncryption.KMS,
            encryption_key=kms.Key(self, "SecureKey")
        )

        # Verify KMS key is properly configured
        if not bucket.encryption_key:
            raise ValueError("KMS key not properly configured")

        # Output key ARN for reference
        CfnOutput(self, "KMSKeyArn", value=bucket.encryption_key.key_arn)