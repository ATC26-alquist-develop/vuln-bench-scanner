from aws_cdk import (
    core,
    aws_s3 as s3,
    aws_s3_deployment as s3deploy,
    aws_s3_bucket_public_access,
    aws_s3_bucket_props,
    aws_s3_object_lock as obj_lock,
    aws_s3_deletion_policy,
    aws_s3_encryption as s3_encryption
)

class S3BucketStack(core.Stack):

    def __init__(self, app: core.App, id: str, **kwargs) -> None:
        super().__init__(app, id, **kwargs)

        # Create S3 bucket with secure defaults
        self.bucket = s3.Bucket(
            self,
            "SecureWebAppBucket",
            bucket_name=f"secure-webapp-bucket-{core.StackSamGeneration.generate_stack_id(self)}",
            encryption=s3_encryption.CfnServerSideEncryptionConfiguration(
                rule=s3_encryption.CfnServerSideEncryptionRule(
                    apply_server_side_encryption_by_default=s3_encryption.CfnServerSideEncryptionRule.ApplyServerSideEncryptionByDefault(
                        s3_encryption.CfnServerSideEncryptionRule.SSEProprietary(
                            status="Enabled",
                            key_protecting_algorithm="AES256"
                        )
                    )
                )
            ),
            removal_policy=core.RemovalPolicy.DESTROY,
            auto_delete_objects=True,
            versioned=True,
            public_access_block=s3_bucket_public_access.BucketPublicAccessBlock(
                block_public_acls=True,
                block_public_policy=True,
                ignore_public_acls=True,
                restrict_public_buckets=True
            ),
            block_public_access=s3.BlockPublicAccess.BLOCK_ALL,
            object_lock_enabled=True,
            object_lock_retention=obj_lock.BucketObjectLockRetentionMode.INFINITE,
            object_lock_enabled_for_all_objects=True,
            server_access_logs_bucket=self.bucket,
            server_access_logs_prefix="access-logs/",
            lifecycle_rules=[
                s3.LifecycleRule(
                    enabled=True,
                    status=s3.LifecycleRule.Status.INACTIVE,
                    expiration=core.Duration.days(30),
                    noncurrent_version_expiration=core.Duration.days(90)
                )
            ],
            auto_delete_objects_versioned=True
        )
        
        # Deploy static content
        s3deploy.BucketDeployment(
            self,
            "DeployStaticContent",
            sources=[s3deploy.Source.asset("./static_content")],
            destination_bucket=self.bucket
        )