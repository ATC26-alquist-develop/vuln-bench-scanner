import os
import logging
from aws_cdk.core import (
    App, Stack,
    aws_s3 as s3
)
from typing import Optional

class SecureS3BucketStack(Stack):
    def __init__(self, scope: App, construct_id: str, **kwargs) -> None:
        """
        Creates a secure S3 bucket with best practices applied.
        
        Args:
            scope (App): The CDK application scope
            construct_id (str): Unique ID for this construct
        """
        super().__init__(scope, construct_id)
        
        # Get region from environment or default to US West (Oregon)
        region = os.environ.get('AWS_REGION', 'us-west-2')
        
        # Enable logging and versioning
        logging = s3.LoggingBucket(
            self, 'LoggingBucket',
            versioned=True,
            enforce_ssl=True,
            auto_delete_logs=True,
            removal_policy=RemovalPolicy.DESTROY
        )
        
        # Create S3 bucket with secure defaults
        bucket = s3.Bucket(
            self, 'SecureBucket',
            versioned=True,
            removal_policy=RemovalPolicy.DESTROY,
            auto_delete_objects=True,
            versioned_object_versions=True,
            enforce_ssl=True,
            logging=LoggingBucket(
                self, 'BucketLogging',
                # Log bucket activity
                removal_policy=RemovalPolicy.DESTROY
            )
        )
        
        # Enable MFA Delete
        bucket_mfa = s3.MFADevice(
            self, 'BucketMFA',
            virtual_environment='Development'
        )
        bucket_mfa.attach(
            lambda _ : bucket_mfa,
            lambda _, __: bucket
        )
        
        # Enable public access blocking
        bucket.add_to_rds_public_access_block(
            BlockPublicAcls=True,
            BlockPublicPolicy=True,
            EnforcePublicReadAccess=False,
            BlockPublicAutomatedTasks=False
        )
        
        # Enable encryption at rest
        bucket.encryption(
            encryption_mode=s3.EncryptionMode.ENCRYPT_ALL,
            rules=[s3.EnvironmentAccessRule(
                owner=SamlUserPrincipal.from_saml_provider(
                    saml_provider_arn='arn:aws:iam::123456789012:saml-provider/MySAMLProvider'
                )
            )]
        )

# Create the app and add the stack
app = App()
SecureS3BucketStack(
    app,
    'SecureS3BucketStack'
)
app.synth()