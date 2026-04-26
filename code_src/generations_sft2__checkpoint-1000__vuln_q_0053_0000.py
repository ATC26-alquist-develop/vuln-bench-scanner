import boto3
import os
from aws_cdk import core
from aws_cdk import aws_lambda as _lambda
from aws_cdk import aws_secretsmanager as secretsmanager

class SecureLambdaStack(core.Stack):
    def __init__(self, scope: core.Construct, id: str, **kwargs):
        super().__init__(scope, id, **kwargs)
        
        # Create a secret in Secrets Manager
        secret = secretsmanager.Secret(self, "UserCredentialsSecret")
        secret.create_secret(
            secret_name="UserCredentials",
            description="Securely store user credentials",
            secret_string=b"your_secret_string_here"
        )
        
        # Create a Lambda function
        lambda_function = _lambda.Function(
            self, "SecureLambda",
            runtime=_lambda.Runtime.PYTHON_3_8,
            handler="lambda_handler",
            code=_lambda.Code.from_asset("lambda"),
            environment={
                "SECRET_NAME": "UserCredentials"
            }
        )
        
        # Grant Lambda permission to access the secret
        secret.grant_read(lambda_function)