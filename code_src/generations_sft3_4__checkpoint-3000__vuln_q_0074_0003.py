from aws_cdk import (
    core as cdk,
    s3 as s3stack,
    kms as kms,
    aws_s3 as s3
)
from constructs import Construct

class SecureS3Stack(s3stack.BucketStack):
    def __init__(self, scope: Construct, id: str, bucket_name: str, 
                 kms_key: kms.Key, **kwargs) -> None:
        """
        Initialize secure S3 bucket with KMS key encryption
        
        Args:
            scope: CDK scope
            id: Stack ID
            bucket_name: S3 bucket name
            kms_key: KMS key for encryption
            **kwargs: Additional stack parameters
        """
        super().__init__(scope, id, bucket_name=bucket_name, **kwargs)
        
        # Validate inputs
        if not isinstance(kms_key, kms.Key):
            raise ValueError("KMS key must be an AWS KMS key")
            
        # Set bucket encryption
        self.bucket.encryption(
            encryption_key=kms_key,
            server_side_encryption_rule=s3.BucketEncryptionRule(
                protocol=s3.BucketEncryptionProtocol.S3,
                status=s3.BucketEncryptionStatusEnabled
            )
        )