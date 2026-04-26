import os
from aws_cdk import core
from s3 import S3BucketWithCors, S3BucketEncryption

class SecureS3Stack(core.Stack):

    def __init__(self, app, id, **kwargs):
        super().__init__(app, id, **kwargs)

        # Get AWS region from environment
        region = os.environ.get('CDK_REGION')
        if not region:
            raise ValueError("AWS_REGION environment variable must be set")

        # Create secure S3 bucket with encryption
        self.bucket = S3BucketWithCors(
            self,
            "SecureFinancialBucket",
            bucket_name=f"secure-finance-bucket-{core.StackSamplify.generate_unique_id()}",  # Use unique ID
            versioned=True,  # Enable versioning
            encryption=S3BucketEncryption.AES256,  # Use AES-256 encryption
            cors=[
                core.CfnBucket.CorsEntryProperty(
                    allowed_headers=['*'],
                    expose_headers=['*'],
                    max_age_seconds=300,
                    allowed_methods=['GET'],
                    allowed_origins=['*']
                )
            ],
            removal_policy=core.RemovalPolicy.DESTROY  # Remove on stack update
        )

        # Add logging
        core.CfnOutput(self, "BucketName", value=self.bucket.bucket_name)
        core.CfnOutput(self, "BucketArn", value=self.bucket.bucket_arn)