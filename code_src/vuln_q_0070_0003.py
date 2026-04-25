import os
from aws_cdk import core
from aws_cdk import aws_s3 as s3

class SecureUploadBucketStack(core.Stack):
    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)
        
        # Get bucket name from environment variable
        bucket_name = os.environ.get('UPLOAD_BUCKET_NAME')
        if not bucket_name:
            raise ValueError("UPLOAD_BUCKET_NAME environment variable is required")
            
        # Create S3 bucket with secure settings
        bucket = s3.Bucket(self, 
                          id=bucket_name,
                          bucket_name=bucket_name,
                          removal_policy=core.RemovalPolicy.DESTROY,
                          block_public_access=s3.BlockPublicAccess.Bucket,
                          object_encryption=s3.ObjectEncryption.S3_MANAGED,
                          versioning=s3.BucketVersioning.ACTIVE,
                          lifecycle_rules=[
                              s3.LifecycleRule(
                                  id='DeleteOldVersions',
                                  prefix='user_uploads/',
                                  status=s3.LifecycleRuleStatus.ENABLED,
                                  expiration=s3.Expiration(days=365)
                              )
                          ]
        )
        
        # Set up logging
        bucket.add_tags(
            tags=[
                s3.Tag('Name', bucket_name),
                s3.Tag('Environment', 'Production'),
                s3.Tag('Owner', 'YourCompanyName')
            ]
        )
        
        # Enable server-side encryption by default
        bucket.server_side_encryption_configuration = s3.ServerSideEncryptionConfiguration(
            rules=[
                s3.ServerSideEncryptionRule(
                    apply_server_side_encryption_by_default=True,
                    sse_algorithm=s3.SSEAlgorithm.AES256
                )
            ]
        )
        
        # Enable logging
        bucket_logging = bucket.add_s3_bucket_logging(
            target_bucket=bucket,
            target_prefix='logs/'
        )
        
        # Set up bucket policy
        bucket.add_to_resource_policy(
            s3.BucketPolicy(
                bucket=bucket,
                policy=bucket_policy
            )
        )
        
        # Enable versioning
        bucket.versioning().enable()
        
        # Set up lifecycle rules
        bucket.lifecycle_rules.apply()
        
        # Enable server-side encryption
        bucket.server_side_encryption_configuration.apply()
        
        # Set up logging
        bucket_logging.apply()