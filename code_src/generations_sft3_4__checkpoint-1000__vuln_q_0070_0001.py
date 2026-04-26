from aws_cdk import core
from aws_cdk import aws_s3 as s3
from aws_cdk import aws_s3_deployment as s3deploy
from aws_cdk import aws_s3_event_notifications as s3en
from aws_cdk import aws_lambda as _lambda
from aws_cdk import aws_lambda_python_alpha as _lambda_python
from aws_cdk import aws_apigateway as apigw

class WebAppStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Create a bucket with default settings
        bucket = s3.Bucket(
            self,
            "WebAppBucket",
            versioned=True,
            encryption=s3.BucketEncryption.S3_MANAGED,
            removal_policy=core.RemovalPolicy.DESTROY
        )

        # Create a Python function to serve the static content
        handler = _lambda_python.PythonFunction(
            self,
            "StaticContentHandler",
            entry="handler",
            index="index.py",
            handler="index.handler",
            runtime=_lambda.Runtime.PYTHON_3_8
        )

        # Deploy static content to the bucket
        s3deploy.BucketDeployment(
            self,
            "DeployStaticContent",
            sources=[s3deploy.Source.asset("static_content")],
            destination_bucket=bucket
        )

        # Set up API Gateway
        api = apigw.RestApi(
            self,
            "WebAppApi",
            rest_api_name="Web Application API"
        )

        # Create a resource for the API
        root_resource = api.root

        # Add a GET method to the root resource
        root_resource.add_method(
            "GET",
            apigw.LambdaIntegration(handler)
        )

        # Set up event notification for the bucket
        s3en.S3EventNotification(
            bucket,
            "StaticContentNotification",
            lambda_function=handler
        )

app = core.App()
WebAppStack(app, "WebAppStack")
app.synth()