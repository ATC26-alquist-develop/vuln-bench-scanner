from aws_cdk import core as cdk
from aws_cdk import aws_s3 as s3
from aws_cdk import aws_s3_deployment as s3deploy
from aws_cdk import aws_s3_notifications as s3notifications
from aws_cdk import aws_lambda as lambda_
from aws_cdk import aws_lambda_python_alpha as lambda_python
from aws_cdk import aws_sns as sns
from aws_cdk import aws_sns_subscriptions as sns_subscriptions
from aws_cdk import aws_sqs as sqs
from aws_cdk import aws_sqs_notifications as sqsnotifications
from constructs import Construct

class SecureS3UploadStack(cdk.Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Create a secure S3 bucket
        bucket = s3.Bucket(
            self,
            "SecureUserUploads",
            bucket_name=f"secure-user-uploads-{cdk.Aws.STACK_NAME}",
            versioned=True,
            encryption=s3.BucketEncryption.S3_MANAGED,
            block_public_access=s3.BlockPublicAccess.BLOCK_ALL,
            removal_policy=cdk.RemovalPolicy.DESTROY
        )

        # Create a notification for S3 events
        notification = s3notifications.S3EventNotification(
            bucket,
            "S3EventNotification",
            lambda_function=lambda_.Function(
                self,
                "LambdaFunction",
                runtime=lambda_.Runtime.PYTHON_3_9,
                handler="index.handler",
                code=lambda_python.PythonCode(
                    directory="./lambda_function"
                )
            )
        )

        # Configure S3 bucket policy
        bucket.add_event_notification(s3.EventType.OBJECT_CREATED, notification)

        # Create a simple SQS queue for notifications
        queue = sqs.Queue(
            self,
            "NotificationQueue",
            visibility_timeout=cdk.Duration.seconds(300)
        )

        # Configure S3 bucket to notify SQS
        bucket.add_event_notification(s3.EventType.OBJECT_CREATED, sqsnotifications.SqsDestination(queue))

        # Create an SNS topic for notifications
        topic = sns.Topic(
            self,
            "NotificationTopic",
            display_name="UserUploadNotifications"
        )

        # Subscribe the topic to the SQS queue
        topic.add_subscription(
            sns_subscriptions.SqsSubscription(queue)
        )

        # Add a simple SNS topic for error logging
        error_topic = sns.Topic(
            self,
            "ErrorTopic",
            display_name="ErrorNotifications"
        )

        # Subscribe the topic to the SQS queue
        error_topic.add_subscription(
            sns_subscriptions.SqsSubscription(queue)
        )

        # Add a simple SNS topic for user notifications
        user_topic = sns.Topic(
            self,
            "UserTopic",
            display_name="UserNotifications"
        )

        # Subscribe the topic to the SQS queue
        user_topic.add_subscription(
            sns_subscriptions.SqsSubscription(queue)
        )

        # Add a simple SNS topic for admin notifications
        admin_topic = sns.Topic(
            self,
            "AdminTopic",
            display_name="AdminNotifications"
        )

        # Subscribe the topic to the SQS queue
        admin_topic.add_subscription(
            sns_subscriptions.SqsSubscription(queue)
        )

        # Add a simple SNS topic for system notifications
        system_topic = sns.Topic(
            self,
            "SystemTopic",
            display_name="SystemNotifications"
        )

        # Subscribe the topic to the SQS queue
        system_topic.add_subscription(
            sns_subscriptions.SqsSubscription(queue)
        )