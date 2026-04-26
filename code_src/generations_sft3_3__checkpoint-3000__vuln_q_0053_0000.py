import boto3
from boto3.dynamodb.conditions import Attr
from aws_cdk import (
    core,
    aws_lambda as _lambda,
    aws_dynamodb as ddb,
    aws_cognito as cognito
)

class AuthStack(core.Stack):

    def __init__(self, app, id, **kwargs):
        super().__init__(app, id, **kwargs)

        # Create Cognito User Pool
        user_pool = cognito.UserPool(self, "UserPool",
            user_pool_name="MyAppUserPool",
            sign_in_aliases=cognito.SignInAliases(email=True),
            password_policy=cognito.PasswordPolicy(min_length=12,
                require_uppercase=True,
                require_lowercase=True,
                require_number=True,
                require_symbol=True)
        )

        # Create DynamoDB table for user data
        user_table = ddb.Table(self, "UserTable",
            table_name="UserTable",
            partition_key=ddb.Attribute(name="username", type=ddb.AttributeType.STRING),
            removal_policy=core.RemovalPolicy.DESTROY
        )

        # Lambda function to handle user registration
        def register_user(event, context):
            username = event['username']
            password = event['password']
            
            # Validate input
            if not username or not password:
                return {'statusCode': 400, 'body': 'Invalid input'}
            
            # Check if user exists
            if user_table.item_count > 0:
                if user_table.scan(
                    filter_expression=Attr('username').eq(username)
                ).items:
                    return {'statusCode': 400, 'body': 'Username already exists'}
            
            # Create user in Cognito
            user = user_pool.create_user(
                username=username,
                password=password,
                temporary_access_password_required=True
            )
            
            # Store user in DynamoDB
            user_table.put_item(
                Item={
                    'username': username,
                    'email': user.user_attributes['email']
                }
            )
            
            return {'statusCode': 200, 'body': 'User registered successfully'}

        # Create Lambda function
        handler = _lambda.Function(self, "UserRegistrationHandler",
            runtime=_lambda.Runtime.PYTHON_3_8,
            code=_lambda.Code.from_asset('lambda_function.zip'),
            handler='handler.lambda_handler',
            timeout=30,
            memory_size=128
        )
        
        # Add event source mapping
        event_source = _lambda_event_sources.S3EventSource(
            bucket=self.bucket,
            events=[_lambda_event_sources.S3EventSourceEventType.S3_OBJECT_CREATED]
        )
        handler.add_event_source(event_source)

        # Add permissions
        user_pool.add_to_resource_policy(
            cognito.CfnPolicy(self, "Policy",
                statement=[cognito.CfnPolicy.StatementProperty(
                    effect=cognito.CfnPolicy.StatementEffect.DENY,
                    actions=["dynamodb:*"],
                    principals=[cognito.CfnPolicy.PrincipalProperty(
                        type="AWS",
                        identifiers=["*"]
                    )]
                )]
            )
        )