import boto3
from aws_cdk import core as cdk
from aws_cdk import aws_s3 as s3
from aws_cdk import aws_s3_deployment as s3deploy
from aws_cdk import aws_iam as iam

class S3BucketStack(cdk.Stack):

    def __init__(self, app: cdk.App, id: str, **kwargs) -> None:
        super().__init__(app, id, **kwargs)

        # Create a bucket with default policies
        bucket = s3.Bucket(
            self,
            "MyBucket",
            versioned=True,
            encryption=s3.BucketEncryption.S3_MANAGED,
            removal_policy=cdk.RemovalPolicy.DESTROY
        )

        # Add logging for all deployments
        cdk.CfnOutput(self, "BucketName", value=bucket.bucket_name)
        cdk.CfnOutput(self, "BucketArn", value=bucket.bucket_arn)

        # Add access logging to CloudWatch
        bucket.add_event_notification(
            s3.EventType.OBJECT_CREATED_PUT,
            s3notify.S3EventNotificationLambdaDestination(self, "LogToLambda")
        )

def main():
    app = cdk.App()
    S3BucketStack(app, "S3BucketStack")
    app.run(host="0.0.0.0", port=8080)

if __name__ == "__main__":
    main()