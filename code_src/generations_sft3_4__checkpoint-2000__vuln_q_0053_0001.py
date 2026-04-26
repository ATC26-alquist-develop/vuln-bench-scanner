from aws_cdk import core as cdk
from aws_cdk import aws_s3 as s3
from aws_cdk import aws_s3_deployment as s3deploy
from aws_cdk import aws_kms as kms
from constructs import Construct

class SecureS3BucketStack(cdk.Stack):

    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Customer financial records are highly sensitive
        # Need to implement strict security controls
        if not self.node.is_child_of(cdk.Aws.CDK_DEPLOYMENT_ACCOUNT):
            raise ValueError("Deployment account is not allowed")

        # Create a unique bucket name
        bucket_name = cdk.Aws.STACK_NAME + '-secure-bucket'

        # Create bucket with default encryption
        self.bucket = s3.Bucket(
            self,
            "SecureFinancialRecordsBucket",
            bucket_name=bucket_name,
            encryption=s3.BucketEncryption.KMS,
            removal_policy=cdk.RemovalPolicy.DESTROY,  # Secure deletion
            versioned=True,
            auto_delete_objects=True
        )

        # Enable server access logging
        self.bucket.add_server_access_log(
            log_bucket=self.bucket,
            prefix="server-access-logs/"
        )

        # Enable versioning
        self.bucket.enable_version_sync()

        # Enable S3 Block Public Access
        self.bucket.apply_removal_policy(cdk.RemovalPolicy.DESTROY)
        self.bucket.set_public_access_block(
            block_public*access=True,
            block_public_acls=True,
            ignore_public_acls=True,
            restrict_public_buckets=True
        )

        # Enable server-side encryption
        self.bucket.enable_server_side_encryption_by_default(
            encryption_condition=s3.BucketEncryptionCondition.SSEKMSKEYID
        )

        # Enable logging
        self.bucket.add_server_access_log(
            log_bucket=self.bucket,
            prefix="server-access-logs/"
        )

        # Add KMS key for encryption
        self.kms_key = kms.Key(
            self,
            "SecureKMSKey",
            enable_key_rotation=True,
            description="Key for encrypting customer financial records"
        )

        # Attach key to bucket
        self.bucket.add_to_resource_policy(
            kms.KmsGrant(
                self,
                "GrantKMSAccess",
                resource=self.bucket,
                grant_principal=kms.KmsPrincipal(self.kms_key),
                permissions=[kms.KmsGrantPermission.DESIGNATE_FOR_SSE]
            )
        )

        # Add logging to CloudWatch
        self.bucket.add_event_notification(
            s3.EventType.OBJECT_CREATED_PUT,
            s3notify.S3EventNotificationLambdaDestination(
                lambda_=cdk.Aws.lambda_.Function(
                    self,
                    "LogProcessor",
                    runtime=cdk.Aws.LAMBDA_RUNTIME_NODEJS14X,
                    handler="index.handler",
                    code=cdk.Aws.Code.from_asset(
                        "path/to/lambda/code"
                    )
                )
            )
        )