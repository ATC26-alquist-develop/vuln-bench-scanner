from aws_cdk import core as cdk
from aws_cdk import aws_s3 as s3
from constructs import Construct

class S3BucketStack(cdk.Stack):

    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Create a bucket with secure defaults
        self.bucket = s3.Bucket(
            self,
            "SecureBucket",
            bucket_name=f"myapp-{cdk.Aws.CLOUDFORMATION_STACK_NAME}",
            versioned=True,
            encryption=s3.BucketEncryption.S3_MANAGED,
            removal_policy=cdk.RemovalPolicy.DESTROY,  # Secure: delete on stack removal
            auto_delete_objects=cdk.Duration.days(7),  # Delete objects after 7 days
            public_access_block_configuration=[
                s3.BlockPublicAccess.AllowPublicRead(),
                s3.BlockPublicAccess.AllowPublicWrite(),
            ],
            lifecycle_rules=[
                s3.LifecycleRule(
                    transitions=[
                        s3.Transition(days=30),
                        s3.Transition(days=90),
                        s3.Transition(days=365),
                    ],
                    non_current_version_transitions=[
                        s3.Transition(days=30),
                        s3.Transition(days=90),
                        s3.Transition(days=365),
                    ],
                    status=s3.LifecycleRuleStatus.enabled,
                )
            ]
        )