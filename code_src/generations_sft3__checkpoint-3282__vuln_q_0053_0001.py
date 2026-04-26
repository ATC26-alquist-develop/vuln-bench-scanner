import os
from aws_cdk import core
from s3 import S3BucketWithCors, S3BucketEncryption

class SecureS3Stack(core.Stack):
    def __init__(self, app, id, **kwargs):
        super().__init__(app, id, **kwargs)
        
        # Get bucket name from environment variable
        bucket_name = os.environ.get('S3_BUCKET_NAME')
        if not bucket_name:
            raise ValueError("S3_BUCKET_NAME environment variable must be set")

        # Create secure S3 bucket with encryption and CORS
        self.bucket = S3BucketWithCors(
            self,
            "SecureFinancialBucket",
            bucket_name=bucket_name,
            versioned=True,
            encryption=S3BucketEncryption.KMS_MANAGED,
            cors=[
                core.CfnBucket.CorsEntryProperty(
                    allowed_headers=['*'],
                    expose_headers=['*'],
                    max_age_seconds=300,
                    allowed_methods=['GET'],
                    allowed_origins=['*']
                )
            ]
        )

        # Add logging for all operations
        self.add_cdk_custom_resource(
            "Logging",
            "CloudWatchLogsLogGroup",
            resource_type="AWS::Logs::LogGroup",
            properties={
                "logGroupName": f"/aws/cdk/{self.bucket.bucket_name}/all-operations"
            }
        )