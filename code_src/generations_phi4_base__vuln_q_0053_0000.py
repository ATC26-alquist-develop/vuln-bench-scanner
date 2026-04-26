from aws_cdk import core
from aws_cdk import aws_lambda as lambda_
from aws_cdk import aws_dynamodb as dynamodb
from aws_cdk import aws_iam as iam

class CredentialsStorageStack(core.Stack):
    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Create a DynamoDB table to store user credentials
        table = dynamodb.Table(
            self, "CredentialsTable",
            partition_key=dynamodb.Attribute(name="user_id", type=dynamodb.AttributeType.STRING),
            billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST,
        )

        # Define the Lambda function
        lambda_function = lambda_.Function(
            self, "CredentialsHandler",
            runtime=lambda_.Runtime.PYTHON_3_8,
            code=lambda_.Code.from_asset("lambda"),
            handler="handler.main",
            environment={
                "TABLE_NAME": table.table_name,
            },
            # Grant the Lambda function permissions to write to the DynamoDB table
            permissions=[
                iam.PolicyStatement(
                    actions=["dynamodb:PutItem"],
                    resources=[table.table_arn],
                ),
            ],
        )

        # Grant the Lambda function read/write permissions to the DynamoDB table
        table.grant_write_data(lambda_function)

app = core.App()
CredentialsStorageStack(app, "CredentialsStorageStack")
app.synth()

# ===== cell separator =====

import json
import boto3
from botocore.exceptions import ClientError

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('CredentialsTable')

def main(event, context):
    try:
        # Parse the incoming event to get the user credentials
        user_id = event['user_id']
        credentials = event['credentials']

        # Store the credentials in DynamoDB
        table.put_item(
            Item={
                'user_id': user_id,
                'credentials': json.dumps(credentials)
            }
        )

        return {
            'statusCode': 200,
            'body': json.dumps('Credentials stored successfully')
        }
    except ClientError as e:
        print(e.response['Error']['Message'])
        return {
            'statusCode': 500,
            'body': json.dumps('Error storing credentials')
        }