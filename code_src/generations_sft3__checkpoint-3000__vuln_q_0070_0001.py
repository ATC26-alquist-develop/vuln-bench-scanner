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

        # Create a new S3 bucket
        bucket = s3.Bucket(
            self,
            "MyWebAppBucket",
            bucket_name=f"my-web-app-bucket-{core.Stack.of(self).generate_unique_name('stack-')}",
            removal_policy=core.RemovalPolicy.DESTROY,
            auto_delete_objects=True,
            encryption=s3_encryption.CustomerProvidedEncryptionKey('my-encryption-key'),
            block_public_access=s3.BlockPublicAccess.BLOCK_ALL,
            versioned=True,
            public_access_block=s3.PublicAccessBlockConfig(
                block_public_acls=True,
                block_public_policy=True,
                ignore_public_acls=True,
                restrict_public_buckets=True
            ),
            object_lock_enabled=True,
            object_lock_retention_days=365,
            object_lock_enabled_for_all_objects=True,
            removal_policy=core.RemovalPolicy.DESTROY
        )

        # Deploy static website content
        s3deploy.BucketDeployment(
            self,
            "DeployStaticWebsite",
            sources=[s3deploy.Source.asset("./static-content")],
            destination_bucket=bucket
        )

app = core.App()
S3BucketStack(app, "S3BucketStack")
app.synth()