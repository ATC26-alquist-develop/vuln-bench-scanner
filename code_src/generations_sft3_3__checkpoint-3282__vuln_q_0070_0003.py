import os
from aws_cdk import (
    core,
    aws_s3 as s3,
    aws_s3_deployment as s3deploy,
    aws_s3_bucket_props as bucket_props
)
from typing import Optional

class SecureS3UploadStack(core.Stack):

    def __init__(self, app: core.App, id: str, **kwargs) -> None:
        super().__init__(app, id, **kwargs)

        # Get bucket name from environment variable
        bucket_name = os.environ.get('S3_BUCKET_NAME')
        if not bucket_name:
            raise ValueError("S3_BUCKET_NAME environment variable must be set")

        # Create bucket with secure defaults
        self.bucket = s3.Bucket(
            self,
            "SecureUserUploadBucket",
            bucket_name=bucket_name,
            versioned=True,  # Enable object versioning
            encryption=s3.BucketEncryption.KMS,  # Enable server-side encryption
            removal_policy=core.RemovalPolicy.DESTROY,  # Cleanup on update
            auto_delete_objects=True,  # Delete objects on bucket deletion
            block_public_access=s3.BlockPublicAccess.BLOCK_ALL,  # Block public access
            public_access_block_props=bucket_props.PublicAccessBlockProps(
                block_public_acls=True,  # Block public ACLs
                block_public_policy=True,  # Block public access policy
                restrict_public_buckets=True  # Restrict public buckets
            ),
            server_access_log_bucket=self.bucket,  # Log access to the same bucket
            server_access_log_prefix="access-logs/",
            versioning_configuration=s3.VersioningConfiguration(status=s3.VersioningStatusEnabled),
            lifecycle_rules=[
                s3.LifecycleRule(
                    enabled=True,
                    transitions=[
                        s3.Transition(
                            transition_to=s3.TransitionStorageClass.GLACIER,
                            transition_after="365days"
                        )
                    ]
                )
            ]
        )

        # Create deployment bucket for uploads
        self.upload_bucket = s3deploy.BucketDeployment(
            self,
            "UploadBucketDeployment",
            sources=[s3deploy.Source.asset("./user_uploads")],
            destination_bucket=self.bucket
        )