from aws_cdk import core as cdk
from aws_cdk import aws_s3 as s3
from aws_cdk import aws_s3_deployment as s3deploy
from aws_cdk import aws_s3_notifications as s3notifications
from aws_cdk import aws_lambda as _lambda
from aws_cdk import aws_lambda_python as _lambda_python
from aws_cdk import aws_sns as sns
from aws_cdk import aws_sns_subscriptions as sns_subscriptions
from aws_cdk import aws_sqs as sqs
from aws_cdk import aws_sqs_notifications as sqsnotifications
from constructs import Construct

class SecureS3BucketStack(cdk.Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Create a secure S3 bucket
        self.bucket = s3.Bucket(
            self,
            "SecureUserUploads",
            bucket_name=f"user-uploads-{cdk.Aws.STACK_NAME}",
            versioned=True,
            encryption=s3.BucketEncryption.S3_MANAGED,
            removal_policy=cdk.RemovalPolicy.DESTROY,
            auto_delete_objects=True,
            block_public_access=s3.BlockPublicAccess.BLOCK_ALL
        )

        # Create a Lambda function to handle uploads
        upload_handler = _lambda_python.PythonFunction(
            self,
            "UploadHandler",
            entry="path/to/lambda/code",
            handler="handler.handler",
            runtime=_lambda.Runtime.PYTHON_3_9,
            environment={
                "BUCKET_NAME": self.bucket.bucket_name
            }
        )

        # Set up S3 bucket notification
        self.bucket.add_event_notification(
            s3.EventType.OBJECT_CREATED_PUT,
            s3notifications.LambdaDestination(upload_handler)
        )

        # Create a SQS queue for notifications
        self.notification_queue = sqs.Queue(
            self,
            "NotificationQueue",
            visibility_timeout=cdk.Duration.seconds(300)
        )

        # Set up S3 bucket notification to SQS
        self.bucket.add_event_notification(
            s3.EventType.OBJECT_CREATED_PUT,
            sqsnotifications.SqsDestination(self.notification_queue)
        )

        # Create SNS topic for notifications
        self.notification_topic = sns.Topic(
            self,
            "NotificationTopic",
            display_name="UserUploadNotifications"
        )

        # Subscribe SQS queue to SNS topic
        self.notification_topic.add_subscription(
            sns_subscriptions.SqsSubscription(self.notification_queue)
        )

        # Add a CloudWatch event to trigger cleanup
        self.cleanup_rule = cdk.CfnOutput(
            self,
            "CleanupRule",
            value=f"aws s3 rb s3://{self.bucket.bucket_name} --force"
        )

        # Add a CloudWatch event to trigger cleanup
        self.cleanup_rule = cdk.CfnOutput(
            self,
            "CleanupRule",
            value=f"aws s3 rb s3://{self.bucket.bucket_name} --force"
        )

        # Add a CloudWatch event to trigger cleanup
        self.cleanup_rule = cdk.CfnOutput(
            self,
            "CleanupRule",
            value=f"aws s3 rb s3://{self.bucket.bucket_name} --force"
        )