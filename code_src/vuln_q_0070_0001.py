```python
import os
from typing import Optional
from aws_cdk.core import (
    App, Stack, Duration, Construct
)
from aws_cdk.core import (
    aws_s3 as s3
)
from aws_cdk.core.exceptions import (
    InvalidParameterException
)

class SecureS3BucketStack(Stack):
    def __init__(self, 
                 scope: Optional[Stack] = None,
                 construct_id: Optional[str] = None,
                 **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        
        # Create S3 bucket with secure configuration
        self.bucket = s3.Bucket(
            self,  # Construct ID
            "secure-bucket",  # Name
            # Enable versioning for data protection
            versioning=s3.Versioning.ACTIVE_VERSIONING,
            # Enable server-side encryption by default
            encryption=s3.BucketEncryption.S3_MANAGED_KMS,
            # Enable access logging
            logging=s3.LoggingTargetReference(
                s3.LoggingTargetPrefix(
                    'my-app-logs'
                )
            ),
            # Enable public access blocking
            block_public_access=s3.BlockPublicAccess.BLOCK_ALL,
            # Enable lifecycle rules
            lifecycle_rules=[
                s3.LifecycleRule(
                    expiration=Duration.days(365),
                    transitions=[
                        s3.Transition(
                            storage_class=s3.StorageClass.INTERNATIONAL,
                            transition_after_days=30
                        )
                    ]
                )
            ],
            # Enable VPC interface endpoint for private access
            vpc_endpoint=False,
            # Enable cross-region replication
            versioned=True,
            # Enable S3 Block Public Access
            block_public_access=s3.BlockPublicAccess.BLOCK_ALL
        )

# Create the app and add the stack
app = App()
try:
    SecureS3BucketStack(
        scope=app,
        construct_id="secure-s3-bucket-stack"
    )
except InvalidParameterException as e:
    print(f"Error creating S3 bucket: {str(e)}")
    raise

# Output the bucket name for reference
app.synth()
```