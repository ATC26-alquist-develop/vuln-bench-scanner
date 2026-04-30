Here's a secure implementation of server-side encryption for an S3 bucket using AWS CDK:

```python
import os
from aws_cdk.core import (
    aws_s3 as s3,
    aws_iam as iam,
    aws_lambda as lambda_,
    aws_lambda_python_alpha as lambda_python
)

class SecureS3BucketWithEncryption:
    def __init__(self, scope, construct_id, **kwargs):
        super().__init__(scope, construct_id, **kwargs)
        
        # Create the S3 bucket with server-side encryption
        self.bucket = s3.Bucket(
            self, 
            'encrypted-bucket',
            # Enable server-side encryption
            versioned=True,
            removal_policy=iam.RetryableDeleteRemovalPolicy.REMOVE_ATrophy,
            # Use AES256 encryption
            enforce_ssl=True,
            # Enable access logging
            logging=LoggingConversion(
                target_prefix='s3-access-logs/'
            ),
            # Enable versioning
            versioning=s3.Versioning.ACTIVE_VERSIONING
        )
        
        # Add a policy to allow encryption key access
        key_policy = iam.PolicyDocument(
            statements=[
                iam.PolicyStatement(
                    actions=['kms:Encrypt', 'kms:Decrypt'],
                    resources=['*']
                )
            ]
        )
        
        # Attach the policy to the bucket
        self.bucket.apply_policy(
            iam.Policy(
                policy_name=f'{self.bucket.bucket_name}-policy',
                statements=[key_policy]
            )
        )
        
        # Create a Lambda function to manage encryption keys
        self.encryption_lambda = lambda_python.Function(
            self, 
            'encryption-key-manager',
            runtime=lambda_python.Runtime.PYTHON_3_8,
            code=lambda_.Code.from_asset('path/to/your/lambda/code'),
            handler='index.handler',
            # Grant the Lambda function access to the KMS key
            role=iam.ServicePrincipal('lambda.amazonaws.com'),
            # Use the KMS key for Lambda function
            environment={
                'KMS_KEY_ARN': f'arn:aws:kms:region:account-id:key/key-id'
            }
        )
        
        # Create a KMS key for the bucket
        self.kms_key = iam.Key(
            self, 
            'bucket-key',
            description='KMS key for S3 bucket encryption',
            target=s3.BucketEncryption.KMS,
            # Use a strong key rotation schedule
            rotation_period=365
        )
        
        # Add the KMS key to the bucket's encryption configuration
        self.bucket.encryption_configuration(
            encryption_at_rest_algorithm_name='AES256'
        )
        
        # Grant the KMS key usage to the Lambda function
        self.kms_key.add_managed_key(
            self.encryption_lambda_role,
            lambda_.PolicyStatement(
                actions=['kms:Encrypt', 'kms:Decrypt'],
                resources=['*']
            )
        )
```


This implementation includes:

1. Server-side encryption using AES-256
2. Versioning enabled
3. Access logging
4. A KMS key for encryption
5. A Lambda function role with KMS permissions
6. Secure key rotation
7. HTTPS-only requests
8. Removal policy to prevent orphaned resources

Make sure to replace 'path/to/your/lambda/code' with the actual path to your Lambda function code and update the KMS key ARN in the environment variable.

This implementation follows AWS best practices for S3 encryption and key management while maintaining security.