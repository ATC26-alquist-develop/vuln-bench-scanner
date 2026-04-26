from aws_cdk import (
    core,
    aws_s3 as s3,
    aws_s3_deployment as s3deploy,
    aws_s3_bucket_public_access,
    aws_s3_bucket_props,
    aws_s3_object_lock as obj_lock,
    aws_s3_deletion_policy
)

class S3BucketStack(core.Stack):

    def __init__(self, app: core.App, id: str, **kwargs) -> None:
        super().__init__(app, id, **kwargs)

        # Create a new S3 bucket
        bucket = s3.Bucket(
            self,
            "MyWebAppBucket",
            bucket_name=f"my-web-app-bucket-{core.StackSamGeneration.generate_stack_id()}",
            removal_policy=core.RemovalPolicy.DESTROY,
            auto_delete_objects=True,
            versioned=True,
            encryption=s3.BucketEncryption.KMS_MANAGED,
            block_public_access=s3.BlockPublicAccess(
                blocks_public_acls=True,
                blocks_public_policy=True,
                restrict_public_buckets=True
            ),
            object_lock_enabled=True,
            object_lock_retention_days=30,
            object_lock_enabled_for_all_objects=True
        )

        # Deploy static website content
        s3deploy.BucketDeployment(
            self,
            "DeployWebsite",
            sources=[s3deploy.Source.asset("./static-content")],
            destination_bucket=bucket
        )

        # Add CORS configuration
        bucket.add_cors_rule(
            allowed_methods=[s3.HttpMethods.GET],
            max_age_seconds=3000,
            allowed_origins=["*"],
            allowed_headers=["*"]
        )

        # Add versioning
        bucket.enable_versioning()

        # Add object lock
        obj_lock.VersioningConfig(
            self,
            "ObjectLockConfig",
            default_retention=obj_lock.RetentionDays.ONE_YEAR,
            enabled=True
        )

        # Add logging
        log_bucket = s3.Bucket(
            self,
            "BucketLogging",
            bucket_name=f"my-web-app-logs-{core.StackSamGeneration.generate_stack_id()}",
            logging_config=s3.BucketLoggingConfig(
                logging_enabled=s3.BucketLoggingConfigProps(
                    target_bucket=bucket,
                    target_key="s3-logs"
                )
            )
        )

app = core.App()
S3BucketStack(app, "S3BucketStack")
app.run()