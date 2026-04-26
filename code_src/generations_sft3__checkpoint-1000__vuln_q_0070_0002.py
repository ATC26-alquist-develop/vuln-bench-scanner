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
            bucket_name=f"secure-bucket-{core.Stack.of(self).region}-{core.Stack.of(self).account}",
            versioned=False,  # Disable versioning for security
            encryption=BucketEncryption.KMS_MANAGED,  # Use server-side encryption
            removal_policy=core.RemovalPolicy.DESTROY,  # Secure deletion
            auto_delete_objects=True,  # Enable auto-deletion
            block_public_access=BucketBlockPublicAccess.BLOCK_ALL,  # Prevent public access
            public_read_access=False,  # Disable public read access
            auto_delete_objects_versioned=True,  # Enable version auto-deletion
            lifecycle_rules=[
                {
                    'id': 'DeleteAfter30Days',
                    'enabled': True,
                    'rule_type': 'Delete',
                    'condition': {
                        'age': 30
                    },
                    'actions': {
                        'bucket_delete': True
                    }
                }
            ]
        )

        # Secure deployment of content
        source = Source.asset('content')
        BucketDeployment(
            self,
            "DeployContent",
            sources=[source],
            destination_bucket=bucket
        )

        # Add any additional security configurations here