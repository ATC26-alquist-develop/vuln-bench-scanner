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
            bucket_name=f"secure-finance-bucket-{core.StackSamplify.generate_stack_id(self)}",
            versioned=True,
            encryption=S3BucketEncryption.KMS_MANAGED,
            cors=[
                core.CfnBucket.CorsEntryProperty(
                    allowed_headers=["*"],
                    expose_headers=["*"],
                    max_age_seconds=300,
                    allowed_methods=["GET"],
                    allowed_origins=["*"]
                )
            ]
        )

        # Add bucket policy to restrict access
        self.bucket.add_bucket_policy(
            core.BucketPolicyStatement(
                principals=["*"],
                actions=["s3:GetObject"],
                resources=[f"arn:aws:s3:::{self.bucket.bucket_name}*"],
                conditions={
                    "StringLike": {
                        "s3:x-amz-acl": ["bucket-owner-full-control"]
                    }
                }
            )
        )

        # Add logging to CloudWatch
        logging_bucket = self.bucket.node.default_child
        logging_bucket.logging_enabled = core.LogsLogBucketLoggingEnabledProperty(
            enabled=True,
            log_bucket=self.bucket
        )