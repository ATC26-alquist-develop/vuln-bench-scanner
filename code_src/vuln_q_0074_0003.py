```python
import boto3
from typing import Optional
from aws_cdk.core import (
    IStack, 
    Construct, 
    aws_s3 as s3,
    aws_kms as kms
)
from my_project import MyCustomValidation

class KMSEnabledS3Bucket(S3Bucket):
    """
    Custom S3 bucket class with KMS encryption enabled
    """
    def __init__(self, 
                 scope: IStack,
                 construct_id: str,
                 **kwargs: dict) -> None:
        super().__init__(scope=scope, construct_id=construct_id, **kwargs)
        
        # Validate input parameters
        MyCustomValidation.validate_s3_bucket_params(kwargs)
        
        # Create KMS key
        key = kms.Key(
            self, 
            "S3BucketKMSKey",
            description=f"KMS key for {self.bucket_name}",
            enable_key_rotation=True,
            removal_policy=aws_cdk.RemovalPolicy.DESTROY
        )
        
        # Enable default encryption with KMS
        self.encryption = s3.BucketEncryption(
            enabled=True,
            encryption_configuration=s3.EncryptionConfiguration(
                rules=[
                    s3.EncryptionRule(
                        priority=1,
                        s3_object_encryption_algorithm=s3.EncryptionAlgorithm.AEAD,
                        s3_object_kms_master_key_id=key.arn
                    )
                ]
            )
        )

    def _before_destroy(self) -> None:
        """
        Clean up KMS key before destroying the bucket
        """
        kms.Key(self, "KMSKeyToDelete").delete()
```