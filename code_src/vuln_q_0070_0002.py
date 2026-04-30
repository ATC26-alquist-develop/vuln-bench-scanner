```python
import aws_cdk as cdk
from aws_cdk import aws_s3 as s3
from aws_cdk.core import Duration, RetentionDays
import os

class SecureS3Bucket(cdk.Stack):
    def __init__(self, scope: cdk.Construct, id: str, bucket_name: str, **kwargs):
        super().__init__(scope, id, **kwargs)
        
        # Get credentials from environment variables
        aws_access_key_id = os.environ.get('AWS_ACCESS_KEY_ID')
        aws_secret_access_key = os.environ.get('AWS_SECRET_ACCESS_KEY')
        aws_session_token = os.environ.get('AWS_SESSION_TOKEN')
        
        if not all([aws_access_key_id, aws_secret_access_key, aws_session_token]):
            raise ValueError("AWS credentials must be set in environment variables")
            
        # Create bucket with secure defaults
        bucket = s3.Bucket(self, 
                         id=bucket_name,
                         removal_policy=cdk.RemovalPolicy.DESTROY,  # Use with caution
                         block_public_access=s3.BlockPublicAccess.BLOCK_ALL,
                         versioning=s3.BucketVersioning.ENABLED,
                         encryption=s3.BucketEncryption.S3_MANAGED,
                         lifecycle_rules=[
                             s3.RuleStatement(
                                 actions=[s3.RemoveObjectsAction(Objects=[s3.ObjectVersion(bucket_name, '/*'))]),
                                 # Automatically delete objects older than 30 days
                                 s3.Condition('Age', '>=' + str(30)))
                         ],
                         # Enable logging
                         logging=s3.BucketLogging(
                             target=s3.LoggingTarget(
                                 bucket_name,
                                 prefix='logs/'
                             )
                         )
                         )
        
        # Set bucket policy (example - adjust as needed)
        bucket.add_to_resource_policy(
            s3.BucketPolicyStatement(
                actions=['s3:GetObject', 's3:ListBucket'],
                resources=[f'arn:aws:s3:::{bucket_name}'],
                principals=[cdk.AwsPrincipal('service', 'amplify.amazonaws.com')],
                condition=s3.Condition('StringEquals', 'aws:SourceArn', 'arn:aws:amplify:*')
            )
        )
```