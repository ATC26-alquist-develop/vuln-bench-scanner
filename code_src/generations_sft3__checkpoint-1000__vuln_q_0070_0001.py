from aws_cdk import core
from aws_cdk import aws_s3 as s3
from aws_cdk import aws_s3_deployment as s3_deployment
from aws_cdk import aws_s3_notifications as s3_notifications
from aws_cdk import aws_lambda as _lambda
from aws_cdk import aws_lambda_python as _lambda_python
from aws_cdk import aws_apigateway as apigw

class WebAppStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Create a bucket with public read access
        bucket = s3.Bucket(
            self,
            "WebAppBucket",
            versioned=True,
            public_read_access=True
        )

        # Create a Lambda function
        handler = _lambda_python.PythonFunction(
            self,
            "Handler",
            entry="lambda_function",
            index="index.py",
            handler="index.handler"
        )

        # Deploy static content to S3
        s3_deployment.BucketDeployment(
            self,
            "DeployStaticContent",
            sources=[s3_deployment.Source.asset("static_content")],
            destination_bucket=bucket
        )

        # Set up API Gateway
        api = apigw.LambdaRestApi(
            self,
            "ApiGateway",
            handler=handler
        )

        # Set up S3 notification for Lambda
        notification = s3_notifications.LambdaDestination(handler)
        bucket.add_event_notification(s3.EventType.OBJECT_CREATED_PUT, notification)

        # Add a basic security group for the Lambda function
        handler.role.add_to_principal_policy(
            core.PolicyStatement(
                actions=["logs:CreateLogGroup", "logs:CreateLogStream", "logs:PutLogEvents"],
                resources=["arn:aws:logs:*:*:*"]
            )
        )

        # Add a basic security group for the API Gateway
        api.node.default_child.add_property_override(
            "security_group",
            core.SecurityGroup(self, "ApiSecurityGroup", vpc=self.vpc)
        )

        # Add a basic security group for the bucket
        bucket.node.default_child.add_property_override(
            "vpc",
            core.Vpc(self, "Vpc", max_azs=2)
        )