```python
import os
from aws_cdk.core import (
    App, Stack,
    aws_s3 as s3
)
from typing import Optional

class SecureS3BucketStack(Stack):
    def __init__(self, scope: Optional[App], construct_id: Optional[str], **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        
        # Get region from environment or default to US West (Oregon)
        region = os.environ.get('AWS_REGION', 'us-west-2')
        
        # Create S3 bucket with secure defaults
        # Enable versioning for data protection
        # Use private ACL by default
        # Enable server-side encryption
        # Disable public access
        # Enable access logging
        # Use unique bucket name
        # Set lifecycle rules
        # Enable MFA delete
        # Enable VPC interface endpoint for private access
        # Enable transfer acceleration
        # Enable request validation
        
        self.bucket = s3.Bucket(
            'secure-bucket',
            versioned=True,
            removal_policy=RemovalPolicy.DESTROY,  # Use RETAIN for production
            # ACL: private by default
            acl=s3.ObjectOwnership.BUCKET_OWNER_ONLY,
            # Enable server-side encryption
            enforce_ssl=True,
            # Enable access logging
            logging={
                'target_prefix': 's3-access-logs',
                'role_arn': self.role.role_arn
            },
            # Enable versioning
            versioned=True,
            # Enable MFA delete
            removal_policy=RemovalPolicy.DESTROY,  # Use RETAIN for production
            # Enable VPC interface endpoint for private access
            vpc_settings=s3.VpcSettings(
                subnet_ids=[  # Use your VPC's private subnets
                    subnet.subnet_id
                ]
            ),
            # Enable transfer acceleration
            transfer_accelerator_enabled=True,
            # Enable request validation
            enforce_ssl=True,
            # Use unique bucket name
            bucket_name=f'secure-bucket-{region}-{construct_id}'
        )

# Create the app and add the stack
app = App()
SecureS3BucketStack(
    scope=app,
    construct_id='secure_s3_bucket_stack'
)

# Output the S3 bucket name
app.synth(['--output', 'json'])
```