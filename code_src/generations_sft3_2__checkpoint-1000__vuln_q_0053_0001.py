from aws_cdk import core as cdk
from aws_cdk import aws_s3 as s3
from aws_cdk import aws_s3_deployment as s3deploy
from aws_cdk import aws_s3_notifications as s3not
from constructs import Construct
import os

class SecureS3BucketStack(cdk.Stack):

    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Get bucket name from environment variable
        bucket_name = os.environ.get('S3_BUCKET_NAME')
        if not bucket_name:
            raise ValueError("S3_BUCKET_NAME environment variable must be set")

        # Create bucket with secure defaults
        self.bucket = s3.Bucket(
            self,
            "SecureCustomerRecordsBucket",
            bucket_name=bucket_name,
            versioned=True,
            encryption=s3.BucketEncryption.S3_MANAGED,
            removal_policy=cdk.RemovalPolicy.DESTROY,
            auto_delete_objects=True,
            block_public_access=s3.BlockPublicAccess.BLOCK_ALL
        )

        # Create deployment source
        source = s3deploy.Source.asset(
            "customer_financial_records"
        )

        # Create notification for deployment
        self.bucket.add_event_notification(
            s3.EventType.OBJECT_CREATED_PUT,
            s3not.S3EventNotificationLambdaDestination(
                lambda_function=self._create_lambda_function()
            )
        )

        # Add logging
        cdk.CfnOutput(
            self,
            "BucketName",
            value=self.bucket.bucket_name
        )

    def _create_lambda_function(self) -> s3not.S3EventNotificationLambdaDestination:
        """Create a secure Lambda function for notifications"""
        # In a real-world scenario, this would be a properly configured Lambda function
        # For demonstration, we'll use a dummy function
        return s3not.S3EventNotificationLambdaDestination(
            lambda_function=cdk.Fn.import_value("lambda-function-arn")
        )