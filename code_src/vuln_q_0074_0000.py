```python
import os
import logging
from typing import Optional
from aws_cdk.core import (
    aws_s3 as s3,
    aws_iam as iam,
    aws_lambda as lambda_,
    aws_lambda_python_alpha as lambda_python
)
from aws_cdk.core.exceptions import (
    InvalidParameter, MissingParameter, CdkInvalidParameterError
)

class SecureS3BucketStack:
    def __init__(self, scope: Optional['SecureS3BucketStack'] = None, **kwargs) -> None:
        super().__init__(scope, **kwargs)
        
        # Configure logging
        logging.basicConfig(level=logging.INFO)
        logger = logging.getLogger(__name__)
        
        # Get region from environment or default to US West (Oregon)
        region = os.environ.get('AWS_REGION', 'us-west-2')
        
        # Create S3 bucket with encryption and security features
        self.bucket = self._create_secure_s3_bucket(
            'SecureBucket',
            'SecureBucketName',
            region=region
        )

    def _create_secure_s3_bucket(
        self,
        name: str,
        description: str,
        region: str
    ) -> s3.Bucket:
        # Input validation
        if not name or not description or not region:
            raise InvalidParameter('Name, description, and region are required')
        
        # Create bucket with encryption and versioning
        bucket = s3.Bucket(
            name,
            versioned=True,
            removal_policy=s3.RemovalPolicy.DESTROY,
            auto_delete_objects=True,
            # Enable default encryption
            encryption=s3.BucketEncryption.AWS_MANAGED_KMS_KEY,
            # Enable public access blocking
            public_read_access=False,
            public_write_access=False,
            # Enable server-side encryption by default
            versioned=True,
            # Enable versioning
            versioned=True,
            # Enable logging
            logging=LoggingProps(
                target_s3_log_bucket=Name(self.bucket.bucket_name),
                target_prefix='s3-access-logs/'
            )
        )
        
        # Add tags for identification and management
        bucket.add_tags(
            {
                'Name': 'Name',
                'Purpose': 'SecureBucket'
            }
        )
        
        # Create and attach a lifecycle policy
        lifecycle_policy = bucket.add_lifecycle_policy(
            rule=[
                {
                    'id': 'ExpireOldVersions',
                    'prefix': '',
                    'status': 'Enabled',
                    'noncurrent_version_expiration': {
                        'noncurrent_days': 365
                    }
                }
            ]
        )
        
        logger.info(f'Created secure S3 bucket: {name}')
        
        return bucket
```