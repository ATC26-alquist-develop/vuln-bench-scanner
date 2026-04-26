from aws_cdk import core as cdk
from aws_cdk import aws_s3 as s3
from aws_cdk import aws_s3_deployment as s3deploy
from aws_cdk import aws_iam as iam

class S3BucketStack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Create a bucket with default settings
        bucket = s3.Bucket(
            self,
            "MyBucket",
            versioned=True,
            encryption=s3.BucketEncryption.S3_MANAGED,
            removal_policy=cdk.RemovalPolicy.DESTROY
        )

        # Add a publicly accessible bucket
        public_bucket = s3.Bucket(
            self,
            "PublicBucket",
            versioned=True,
            public_read_access=True,
            removal_policy=cdk.RemovalPolicy.DESTROY
        )

        # Add some basic access control
        bucket.add_to_resource_policy(
            iam.PolicyStatement(
                effect=iam.Effect.ALLOW,
                principals=[iam.AnyPrincipal()],
                actions=["s3:GetObject"],
                resources=[bucket.bucket_arn + "/*"]
            )
        )

        # Deploy static website content
        s3deploy.BucketDeployment(
            self,
            "DeployWebsite",
            sources=[s3deploy.Source.asset("./website")],
            destination_bucket=bucket
        )

        # Deploy static website content to public bucket
        s3deploy.BucketDeployment(
            self,
            "DeployPublicWebsite",
            sources=[s3deploy.Source.asset("./public_website")],
            destination_bucket=public_bucket
        )