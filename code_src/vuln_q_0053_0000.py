import os
from aws_cdk.core import (
    aws_lambda as _lambda,
    aws_dynamodb as dynamodb,
    aws_iam as iam,
    aws_events as events
)

class SecureCredentialHandler(_lambda.Function):
    def __init__(self, scope: _lambda.FunctionScope, 
                 id: str, 
                 table: dynamodb.Table, 
                 **kwargs):
        super().__init__(scope, id, **kwargs)
        
        # Use environment variables for sensitive data
        handler = events.Handler(
            target=table,
            event_pattern={
                "version": "1.0",
                "detail": {
                    "event": ["user_login_attempt"]
                }
            }
        )
        
        # Grant minimal necessary permissions
        table.grant_write(data_streams=True, 
                         triggers=handler)
        
        # Create a dead-letter queue for failed invocations
        dlq = dlq_name = f"{self.get_purposeful_name('dlq')}"
        dlq_arn = dlq.grant_invoke_lambda(
            lambda_function=self
        )
        
        # Set up dead-lettering
        self.dead_letter_config = _lambda.LambdaDeadLetterConfig(
            target=dynamodb.Table(
                dlq_arn.split(":")[1],
                removal_policy=RemovalPolicy.DESTROY
            )
        )
        
        # Add environment variables for credentials
        self.environment = {
            'TABLE_NAME': table.table_name
        }

    @staticmethod
    def get_purposeful_name(name: str) -> str:
        """Generate a meaningful name for resources."""
        return f"{name}_{os.environ.get('AWS_ACCOUNT_ID', 'unknown')}"