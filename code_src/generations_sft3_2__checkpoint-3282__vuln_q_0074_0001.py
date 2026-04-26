from aws_cdk import (
    core,
    aws_s3 as s3,
    aws_kms as kms,
    aws_s3_deployment as s3deploy
)

class SecureS3BucketStack(core.Stack):

    def __init__(self, app: core.App, id: str, **kwargs) -> None:
        super().__init__(app, id, **kwargs)

        # Create a KMS key for encryption
        key = kms.Key(self, "SecureKey",
            enable_at_provision_time=False,  # Enable only when needed
            description="Secure key for S3 bucket encryption",
            encryption_key_rotation=True
        )

        # Create an S3 bucket with server-side encryption and KMS key
        bucket = s3.Bucket(self, "SecureBucket",
            bucket_name=f"secure-data-{core.StackSamplify.generate_stack_id()}",
            encryption_key=key,
            server_side_encryption_configuration=[
                s3.ServerSideEncryptionRule(
                    apply_to_referenced_objects_only=True,
                    encryption_method="AES256",
                    storage_class="STANDARD"
                )
            ],
            block_public_access=s3.BlockPublicAccess.BLOCK_ALL
        )

        # Deploy a sample file to the bucket
        s3deploy.BucketDeployment(self, "DeploySample",
            sources=[s3deploy.Source.asset("./sample_data")],
            destination_buckets=[bucket]
        )