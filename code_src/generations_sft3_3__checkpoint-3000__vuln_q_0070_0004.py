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
            encryption=s3.BucketEncryption.KMS,
            removal_policy=cdk.RemovalPolicy.DESTROY
        )

        # Add logging
        cdk.CfnOutput(self, "BucketName", value=bucket.bucket_name)
        cdk.CfnOutput(self, "BucketArn", value=bucket.bucket_arn)

        # Add access logging to CloudWatch
        log_bucket = s3.Bucket(
            self,
            "AccessLogBucket",
            versioned=True,
            encryption=s3.BucketEncryption.KMS,
            removal_policy=cdk.RemovalPolicy.DESTROY
        )
        bucket.add_event_notification(
            s3.EventType.OBJECT_CREATED_PUT,
            s3.NotificationTarget(log_bucket)
        )

        # Add default bucket policies
        bucket.add_to_resource_policy(
            iam.PolicyStatement(
                effect=iam.Effect.ALLOW,
                principals=[iam.AnyPrincipal()],
                actions=["s3:GetObject"],
                resources=[f"{bucket.bucket_arn}/*"]
            )
        )

app = cdk.App()
S3BucketStack(app, "S3BucketStack")
app.synth()