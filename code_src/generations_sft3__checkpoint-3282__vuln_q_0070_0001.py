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
            block_public_access=s3.BlockPublicAccess.BLOCK_ALL,
            public_access_block_configuration={
                "BlockPublicAcls": True,
                "IgnorePublicAcls": True,
                "BlockPublicPolicy": True,
                "RestrictPublicBuckets": True
            },
            object_lock_enabled=True,
            object_lock_retention_days=30,
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

        # Add versioning
        bucket.add_to_resource_policy(
            core.PolicyStatement(
                actions=["s3:PutObject"],
                resources=[f"{bucket.bucket_arn}/*"],
                principals=[core.Principal("allAuthenticatedUsers")],
                effect=core.PolicyEffect.ALLOW
            )
        )

        # Enable CORS
        bucket.add_cors_rule(
            allowed_methods=[s3.HttpCorsMethod.HEAD, s3.HttpCorsMethod.GET],
            max_age_seconds=3000,
            allowed_origins=["*"]
        )

        # Enable S3 Object Lock
        obj_lock.VersioningConfig(
            self,
            "ObjectLockVersioning",
            bucket=bucket
        )

        # Enable server-side encryption
        bucket.enable_server_side_encryption_by_default(
            s3.BucketEncryption.KMS governed=True
        )

        # Enable versioning
        bucket.enable_versioning()

        # Enable logging
        bucket.add_logging_config(
            log_bucket=bucket,
            log_prefix="Logs/"
        )