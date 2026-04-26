from aws_cdk import core
from aws_cdk.aws_s3 import Bucket
from aws_cdk.aws_s3_deployment import (
    BucketDeployment,
    Source
)
from constructs import Construct

class SecureS3BucketStack(core.Stack):

    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Create a secure S3 bucket with proper defaults
        bucket = Bucket(
            self,
            "SecureBucket",
            bucket_name=f"secure-bucket-{self.region}-{self.account}",
            removal_policy=core.RemovalPolicy.DESTROY,  # Secure: Remove on stack update
            versioned=False,  # Disable versioning for security
            encryption=BucketEncryption.KMS_MANAGED,  # Use KMS for encryption
            block_public_access=BucketBlockPublicAccess.BLOCK_ALL,  # Prevent public access
            auto_delete_objects=True,  # Enable auto-deletion
            public_read_access=False,  # Disable public read access
            auto_delete_objects_versioned=True,  # Enable auto-deletion for versions
            lifecycle_rules=[
                {
                    'id': 'DeleteOldVersions',
                    'rule_type': 'Delete',
                    'condition': {
                        'age': 30  # Delete objects older than 30 days
                    },
                    'action': {
                        'type': 'Delete'
                    }
                }
            ]
        )

        # Securely deploy content to the bucket
        source = Source.asset('path/to/your/content')
        BucketDeployment(
            self,
            "DeployContent",
            sources=[source],
            destination_bucket=bucket
        )

        # Add any additional security configurations here
        # For example, you can add logging or monitoring