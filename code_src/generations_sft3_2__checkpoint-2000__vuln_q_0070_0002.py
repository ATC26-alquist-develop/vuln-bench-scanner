from aws_cdk import core as cdk
from aws_cdk import aws_s3 as s3
from constructs import Construct

class SecureS3BucketStack(cdk.Stack):

    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Create a secure S3 bucket with default policies
        bucket = s3.Bucket(
            self,
            "SecureBucket",
            bucket_name=f"secure-bucket-{cdk.Aws.RandomIdentifier()}",
            versioned=True,  # Enable versioning
            encryption=s3.BucketEncryption.KMS_MANAGED,  # Use server-side encryption
            removal_policy=cdk.RemovalPolicy.DESTROY,  # Securely delete on stack removal
            auto_delete_objects=True,  # Enable auto-deletion
            block_public_access=s3.BlockPublicAccess.BLOCK_ALL,  # Block public access
            public_read_access=False,  # Disable public read access
            auto_delete_objects_versioned=True,  # Enable auto-deletion for versions
            lifecycle_rules=[
                s3.LifecycleRule(
                    enabled=True,
                    transitions=[
                        s3.Transition(
                            transition_to=s3.BucketTransitionStorageClass.GLACIER,
                            duration=cdk.Duration.days(365)
                        )
                    ]
                )
            ]
        )

        # Add any additional customizations here