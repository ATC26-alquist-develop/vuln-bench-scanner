import boto3
from boto3.dynamodb.conditions import Attr
from aws_cdk import (
    core,
    aws_lambda as _lambda,
    aws_dynamodb as ddb,
    aws_cognito as cognito
)

class SecureAuthStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Create Cognito User Pool
        user_pool = cognito.UserPool(self, "UserPool",
            user_pool_name="SecureUserPool",
            explicit_auth_flows=[cognito.AuthFlow.PASSWORD_RECOVERY],
            sign_in_aliases=cognito.SignInAliases(email=True),
            auto_verify=[cognito.AttributeType(email=True)]
        )

        # Create DynamoDB table for user data
        user_table = ddb.Table(self, "UserTable",
            partition_key=ddb.Attribute(name="username", type=ddb.AttributeType.STRING),
            billing_mode=ddb.BillingMode.PAY_PER_REQUEST
        )

        # Lambda function to handle user registration
        def register_user(event, context):
            username = event['username']
            password = event['password']
            
            # Validate input
            if not username or not password:
                return {'statusCode': 400, 'body': 'Invalid input'}
            
            # Verify username is unique
            if user_table.table_items.count(Attr('username').eq(username)) > 0:
                return {'statusCode': 409, 'body': 'Username already exists'}
            
            # Create user in Cognito
            user_pool.create_user(
                username=username,
                password=password,
                temporary_password=None,
                user_status=cognito.UserStatus.UNVERIFIED
            )
            
            # Store user in DynamoDB
            user_table.put_item(
                Item={
                    'username': username,
                    'email': event.get('email', ''),
                    'verified': False
                }
            )
            
            return {'statusCode': 201, 'body': 'User registered successfully'}

        # Create Lambda function
        handler = _lambda.Function(
            self, "UserRegistrationHandler",
            runtime=_lambda.Runtime.PYTHON_3_8,
            code=_lambda.Code.from_asset('lambda_function.zip'),
            handler='handler.lambda_handler',
            timeout=30,
            memory_size=128
        )

        # Attach permissions
        user_table.grant_read_write_data(handler)
        user_pool.grant_admin_authentication(handler)