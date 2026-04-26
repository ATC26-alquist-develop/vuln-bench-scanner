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
        self.bucket.add_to_resource_policy(
            core.PolicyStatement(
                actions=["s3:*Object"],
                resources=[f"arn:aws:s3:::{bucket_name}*"],
                principals=[core.Principal("allAuthenticatedUsers")],
                effect=core.PolicyEffect.ALLOW
            )
        )

        # Add specific deny policy for sensitive data
        self.bucket.add_to_resource_policy(
            core.PolicyStatement(
                actions=["s3:GetObject"],
                resources=[f"arn:aws:s3:::{bucket_name}/*"],
                principals=[core.Principal("allAuthenticatedUsers")],
                conditions={
                    "StringLike": {
                        "s3:x-amz-acl": "bucket-owner-full-control"
                    }
                },
                effect=core.PolicyEffect.DENY
            )
        )