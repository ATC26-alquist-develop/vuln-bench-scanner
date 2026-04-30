import os
import logging
from typing import Optional
import boto3
from aws_cdk import (
    core,
    aws_s3 as s3,
    aws_iam as iam,
    aws_sops as sops,
    aws_lambda as lambda_,
    aws_lambda_event_sources as lambda_event_sources,
    aws_lambda_python_alpha as lambda_python_alpha
)

class SecureS3BucketStack(core.Stack):
    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)
        
        # Get bucket name from environment variable
        bucket_name = os.environ.get('S3_BUCKET_NAME')
        if not bucket_name:
            raise ValueError("S3_BUCKET_NAME environment variable must be set")
            
        # Validate bucket name
        if not bucket_name.isalnum() or len(bucket_name) > 63:
            raise ValueError("Invalid S3 bucket name format")
            
        # Create S3 bucket with secure defaults
        self.bucket = s3.Bucket(
            self, 
            bucket_name=bucket_name,
            versioned=True,
            encryption=s3.BucketEncryption.S3_MANAGED_KMS,
            block_public_acls=True,
            block_public_policy=True,
            object_lock_enabled=True,
            object_lock_retention=core.Duration.days(365),
            lifecycle_rules=[
                s3.LifecycleRule(
                    noncurrent_version_expiration=core.Duration.days(365)
                )
            ]
        )
        
        # Create IAM role for Lambda
        lambda_role = iam.Role(
            self, 
            "LambdaExecutionRole",
            assumed_by=iam.ServicePrincipal("lambda.amazonaws.com"),
            managed_policies=[
                iam.ManagedPolicy.from_arn(
                    "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
                )
            ]
        )
        
        # Create Lambda function
        self.lambda_function = lambda_python_alpha.Function(
            self, 
            "SecureS3Handler",
            runtime=lambda_python_alpha.PYTHON_3_8,
            code=lambda_.Code.from_asset("lambda"),
            handler="handler",
            role=lambda_role,
            environment={
                "S3_BUCKET_NAME": bucket_name,
                "SOPS_KEY": os.environ.get('SOPS_KEY')
            }
        )
        
        # Set up SOPS encryption
        sops_key = os.environ.get('SOPS_KEY')
        if not sops_key:
            raise ValueError("SOPS_KEY environment variable must be set")
            
        sops_key_arn = sops.Key.from_key_arn(
            self,
            "SopsKey",
            "arn:aws:sops:us-east-1:123456789012:key/1234567890123456789012345678901234567890"
        )
        
        # Create SOPS encryption configuration
        sops_config = sops.SopsEncryptionConfiguration(
            key=sops_key_arn,
            bucket=self.bucket
        )
        
        # Attach SOPS encryption to bucket
        self.bucket.apply_sops_encryption(sops_config)
        
        # Set up Lambda trigger
        self.lambda_function.add_event_source(lambda_event_sources.S3EventSource(
            self.bucket
        ))

def main():
    # Set up logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    
    # Initialize CDK app
    app = core.App()
    
    # Create stack
    try:
        SecureS3BucketStack(app, "SecureS3BucketStack")
        logger.info("S3 bucket and Lambda function created successfully")
    except Exception as e:
        logger.error(f"Error creating resources: {str(e)}")
        raise

if __name__ == "__main__":
    main()