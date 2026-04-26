import boto3
from aws_cdk import core
from aws_cdk import aws_lambda as _lambda
from aws_cdk import aws_dynamodb as _dynamodb
from aws_cdk import aws_s3 as _s3

class UserCredentialsLambdaStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # DynamoDB Table
        user_credentials_table = _dynamodb.Table(
            self, "UserCredentialsTable",
            partition_key=_dynamodb.Attribute(name="userId", type=_dynamodb.AttributeType.STRING),
            billing_mode=_dynamodb.BillingMode.PAY_PER_REQUEST
        )

        # Lambda Function
        handler = _lambda.Function(
            self, "UserCredentialsHandler",
            runtime=_lambda.Runtime.PYTHON_3_8,
            handler="lambda_function.lambda_handler",
            code=_lambda.Code.from_asset("lambda_function"),
            environment={
                "USER_CREDENTIALS_TABLE_NAME": user_credentials_table.table_name
            }
        )

        # DynamoDB Table Policy
        user_credentials_table.grant_read_write_data(handler)

        # S3 Bucket (Optional: For storing credentials securely)
        # s3_bucket = _s3.Bucket(self, "CredentialsBucket")

        # Add any other necessary resources or configurations here

# ===== cell separator =====

import json
import boto3

def lambda_handler(event, context):
    # Extract user credentials from the event
    user_credentials = json.loads(event['body'])
    user_id = user_credentials['userId']
    password = user_credentials['password']

    # DynamoDB client
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('UserCredentialsTable')

    # Store the credentials in DynamoDB
    response = table.put_item(
        Item={
            'userId': user_id,
            'password': password
        }
    )

    return {
        'statusCode': 200,
        'body': json.dumps('Credentials stored successfully')
    }