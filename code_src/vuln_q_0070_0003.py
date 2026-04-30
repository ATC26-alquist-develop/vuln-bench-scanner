import os
from aws_cdk import (
    core,
    aws_s3 as s3,
    aws_s3_notifications as s3_notifications
)

class SecureUploadBucket(core.Stack):
    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)
        
        # Get bucket name from environment variable
        bucket_name = os.environ.get('UPLOAD_BUCKET_NAME')
        if not bucket_name:
            raise ValueError("UPLOAD_BUCKET_NAME environment variable is required")
            
        # Create S3 bucket with secure configuration
        bucket = s3.Bucket(self, 
            "SecureUploadBucket",
            bucket_name=bucket_name,
            removal_policy=core.RemovalPolicy.RETAIN,
            block_public_access=s3.BlockPublicAccess(
                block_public_acls=True,
                block_public_policy=True,
                ignore_public_acls=False,
                restrict_public_buckets=False
            ),
            versioned=True,
            encryption=s3.BucketEncryption.S3_MANAGED_KEY_ALGORITHM_256,
            notification=s3_notifications.SnsDestination(
                topic=s3_notifications.SnsTopic(stack, "NotificationTopic"),
                role=s3_notifications.SnsRole(stack, "NotificationRole")
            )
        )
        
        # Set bucket policy to restrict access
        bucket.add_to_resource_policy(
            s3.BucketPolicyStatement(
                statement_id="restrict_access",
                effect=s3.BucketPolicyStatement.IAccessibleByObjectNotAllowed,
                principal=s3.Principal.all(),
                actions=["s3:GetObject"],
                resources=[f"{bucket.arn}/*"]
            )
        )
        
        # Enable server-side encryption by default
        bucket.server_side_encryption_configuration = s3.ServerSideEncryptionConfiguration(
            rules=[s3.ServerSideEncryptionApplyServerSideEncryptionRule(
                s3.ServerSideEncryptionRuleStatement(
                    apply_server_side_encryption_by_default=True,
                    sse_algorithm=s3.SSEAlgorithm.SSE_S3_MANAGED
                )
            )]
        )
        
        # Enable versioning
        bucket.versioning().enabled = True
        
        # Set up lifecycle rules
        bucket.add_to_resource_policy(
            s3.BucketLifecycleConfigurationStatement(
                statement_id="lifecycle_rule",
                action="s3:PutBucketLifecycleConfiguration",
                principal="*",
                effect=s3.BucketLifecycleConfigurationStatement.LifeCycleConfigurationEffect.ENABLE,
                condition=s3.BucketLifecycleConfigurationStatement.ConditionFilter(
                    s3.ConditionFilter(
                        s3.FilterByPrefix("user_uploads/")
                    )
                ),
                rules=[
                    s3.RuleStatement(
                        s3.RuleStatement.Filter=s3.FilterByPrefix("user_uploads/"),
                        s3.RuleStatement.Condition=s3.Condition(
                            s3.ComparisonOperator.EQUALS,
                            s3.Key("s3:ObjectExists", "true")
                        ),
                        s3.RuleStatement.Action=s3.RuleStatement.Action(
                            s3.LifecycleActionStatement(
                                Id="TransitionToGlacier",
                                Status=s3.LifecycleActionStatus.ENABLED,
                                Destination=s3.DestinationConfiguration(
                                    Bucket=s3.Bucket(bucket),
                                    StorageClass=s3.StorageClass.GLACIER
                                )
                            )
                        )
                    )
                ]
            )
        )