from aws_cdk import (
    core,
    aws_s3 as s3,
    aws_s3_deployment as s3deploy,
    aws_s3_bucket_public_access,
    aws_s3_bucket_props,
    aws_s3_bucket_versioning
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
            versioned=True
        )

        # Deploy static website content
        s3deploy.BucketDeployment(
            self,
            "DeployWebsite",
            sources=[s3deploy.Source.asset("./static-content")],
            destination_bucket=bucket
        )

        # Configure bucket policies
        bucket.add_to_resource_policy(
            s3.CfnBucketPolicyStatement(
                self,
                "AllowPublicRead",
                effect=s3.CfnBucketPolicyStatement.Effect.ALLOW,
                principals=["*"],
                actions=["s3:GetObject"],
                resources=[f"{bucket.bucket_arn}/*"],
                conditions={
                    "StringLike": {
                        "s3:x-amz-acl": ["bucket-owner-full-control", "public-read"]
                    }
                }
            )
        )

        # Enable versioning
        bucket.versioning_enabled = True

        # Enable website hosting
        bucket.website_index_document = "index.html"
        bucket.website_error_document = "error.html"

        # Enable CORS
        bucket.cors_configuration = s3.CorsConfiguration(
            max_age_seconds=3000,
            origins=["*"],
            allowed_headers=["*"],
            allow_methods=["GET", "HEAD"]
        )
        bucket.add_cors_rule(
            configuration=bucket.cors_configuration
        )