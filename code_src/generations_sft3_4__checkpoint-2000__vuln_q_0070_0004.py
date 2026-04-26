import boto3
from aws_cdk import core as cdk
from aws_cdk import aws_s3 as s3
from aws_cdk import aws_s3_deployment as s3deploy
from aws_cdk import aws_iam as iam

class S3BucketStack(cdk.Stack):

    def __init__(self, app: cdk.App, id: str, **kwargs) -> None:
        super().__init__(app, id, **kwargs)

        # Create bucket with default policies
        bucket = s3.Bucket(
            self,
            "MyBucket",
            versioned=True,
            encryption=s3.BucketEncryption.S3_MANAGED,
            removal_policy=cdk.RemovalPolicy.DESTROY
        )

        # Add logging
        cdk.CfnOutput(self, "BucketName", value=bucket.bucket_name)
        cdk.CfnOutput(self, "BucketArn", value=bucket.bucket_arn)

        # Grant basic access permissions
        bucket.grant_read_write(
            iam.ServicePrincipal("s3.amazonaws.com")
        )

# Usage example
app = cdk.App()
S3BucketStack(app, "S3BucketStack")
app.synth()