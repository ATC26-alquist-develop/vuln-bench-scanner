from aws_cdk import (
    core,
    aws_s3 as s3,
    aws_kms as kms,
    aws_s3_deployment as s3deploy,
    aws_s3_deployment_props as s3deploy_props,
    aws_iam as iam
)

class SecureS3BucketStack(core.Stack):

    def __init__(self, app: core.App, id: str, **kwargs) -> None:
        super().__init__(app, id, **kwargs)

        # Create a KMS key for encryption
        key = kms.Key(self, "SecureKey",
            enable_at_provision_time=True,
            description="Secure key for encrypting S3 bucket contents"
        )

        # Create an S3 bucket with encryption enabled
        bucket = s3.Bucket(self, "SecureBucket",
            bucket_name=f"secure-data-{core.Stack.of(self).generate_unique_name('bucket')}",
            encryption_key=key,
            block_public_access=s3.BlockPublicAccess.BLOCK_ALL,
            removal_policy=core.RemovalPolicy.DESTROY
        )

        # Deploy files to the bucket
        s3deploy.BucketDeployment(self, "DeployFiles",
            sources=[s3deploy.Source.asset("./path/to/your/files")],
            destination_bucket=bucket
        )

        # Attach policy to allow access only from trusted IPs
        bucket.add_to_resource_policy(
            iam.PolicyStatement(
                effect=iam.Effect.ALLOW,
                principals=[iam.AnyPrincipal()],
                actions=["s3:GetObject"],
                resources=[f"{bucket.bucket_arn}/*"],
                conditions={
                    "StringEquals": {
                        f"aws:SourceIp": ["10.0.0.0/8", "172.16.0.0/12", "192.168.0.0/16"]
                    }
                }
            )
        )

        # Add logging
        core.CfnOutput(self, "BucketName", value=bucket.bucket_name)
        core.CfnOutput(self, "BucketArn", value=bucket.bucket_arn)