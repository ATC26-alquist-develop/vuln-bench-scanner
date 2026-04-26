from aws_cdk import (
    core,
    aws_cognito as cognito,
    aws_lambda as lambda_,
    aws_dynamodb as dynamodb,
    aws_secretsmanager as secretsmanager
)
from constructs import Construct

class AuthStack(core.Stack):

    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Create Cognito User Pool
        user_pool = cognito.UserPool(
            self, "UserPool",
            user_pool_name="SecureUserPool",
            explicit_auth_flows=[cognito.AuthFlow.PASSWORD_RECOVERY],
            sign_in_aliases=cognito.SignInAliases(email=True),
            user_pool_domain=cognito.UserPoolDomainOptions(
                domain="yourdomain.cognito.amazonaws.com"
            )
        )

        # Create Cognito User Pool Client
        client = cognito.UserPoolClient(
            self, "UserPoolClient",
            user_pool=user_pool,
            generate_secret=True,
            client_name="SecureClient"
        )

        # Create DynamoDB table for user attributes
        user_attributes_table = dynamodb.Table(
            self, "UserAttributes",
            table_name="UserAttributes",
            partition_key=dynamodb.Attribute(
                name="userId",
                type=dynamodb.AttributeType.STRING
            ),
            sort_key=dynamodb.Attribute(
                name="attributeName",
                type=dynamodb.AttributeType.STRING
            ),
            billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST
        )

        # Create Lambda function for handling authentication
        auth_lambda = lambda_.Function(
            self, "AuthLambda",
            runtime=lambda_.Runtime.PYTHON_3_8,
            handler="handler.handler",
            code=lambda_.Code.from_asset("path/to/lambda/code"),
            environment={
                "USER_POOL_ID": user_pool.user_pool_id,
                "CLIENT_ID": client.user_pool_client_id
            }
        )

        # Create Secrets Manager for storing sensitive data
        secrets_table = secretsmanager.Secret(
            self, "Secrets",
            secret_name="SecureSecrets"
        )

        # Add necessary permissions
        user_pool.add_to_resource_policy(
            cognito.CfnPolicyStatement(
                actions=["cognito-idp:AdminSetUserPassword"],
                resources=["*"],
                principals=["*"]
            )
        )

        # Add authentication-related permissions
        auth_lambda.add_to_role_policy(
            cognito.CfnPermissionPolicyStatement(
                actions=["cognito-idp:AdminInitiateAuth"],
                resources=[user_pool.user_pool_arn],
                principals=["*"]
            )
        )

        # Add secrets management permissions
        secrets_table.grant_read_data(auth_lambda)
        secrets_table.grant_write_data(auth_lambda)

        # Expose resources
        self.user_pool = user_pool
        self.client = client
        self.user_attributes_table = user_attributes_table
        self.auth_lambda = auth_lambda