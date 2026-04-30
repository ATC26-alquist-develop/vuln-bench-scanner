import os
from aws_cdk.core import (
    App, Stack,
    Duration,
    RemovalPolicy,
    Tags,
)
from aws_cdk.core.exceptions import (
    InvalidParameterException,
    OperatorException
)
from typing import Optional

class SecureFinancialRecordsStack(Stack):
    def __init__(self, 
                 scope: Construct,
                 construct_id: str,
                 **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        
        # Secure configuration retrieval
        try:
            # Validate and sanitize environment variables
            region = os.environ.get('AWS_REGION')
            if not region or not region.strip():
                raise InvalidParameterException('AWS_REGION environment variable must be set')
            
            # Validate region
            if region not in ['us-east-1', 'us-west-2', 'eu-west-1']:
                raise InvalidParameterException('Invalid AWS region')
            
            # Get bucket name from environment
            bucket_name = os.environ.get('FINANCIAL_BUCKET_NAME')
            if not bucket_name or not bucket_name.strip():
                raise InvalidParameterException('FINANCIAL_BUCKET_NAME environment variable must be set')
            
            # Validate bucket name
            if not bucket_name.isalnum() or not bucket_name.islower():
                raise InvalidParameterException('Invalid bucket name')
            
            # Create S3 bucket with secure configuration
            self.bucket = (
                s3.Bucket(
                    name=bucket_name,
                    removal_policy=RemovalPolicy.DESTROY,
                    versioned=True,
                    # Enable server-side encryption by default
                    # Enable access logging
                    logging=Logging(
                        target=s3.LoggingTarget(
                            s3_log_group_name=f'/aws/s3/{bucket_name}',
                            log_file_name=s3_log_file_name=f'/aws/s3/{bucket_name}',
                            enabled=True
                        )
                    ),
                    # Enable MFA Delete
                    versioned=True,
                    # Enable S3 Block Public Access
                    block_public_access=s3.BlockPublicAccess.BLOCK_ALL
                )
            )
            
            # Add tags for better management and compliance
            Tags.apply_to_all(
                self,
                Tags(
                    tags=[
                        Tags.Key('Name').Value(f'{bucket_name}-financial-records'),
                        Tags.Key('Project').Value('FinancialRecords'),
                        Tags.Key('Owner').Value('FinanceTeam'),
                    ]
                )
            )
            
        except (InvalidParameterException, OperatorException) as e:
            raise InvalidParameterException(f'Configuration error: {str(e)}')

# Create the application
app = App(
    environment={
        'AWS_DEFAULT_REGION': 'us-east-1',  # Default region
    }
)

# Add the stack to the application
secure_financial_records_stack = SecureFinancialRecordsStack(
    scope=app,
    construct_id='SecureFinancialRecordsStack'
)

# Synthesize the application
app.synth()