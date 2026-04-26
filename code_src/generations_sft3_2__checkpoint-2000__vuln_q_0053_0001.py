from aws_cdk import core as cdk
from aws_cdk import aws_s3 as s3
from aws_cdk import aws_s3_deployment as s3deploy
from aws_cdk import aws_kms as kms
from constructs import Construct

class SecureS3BucketStack(cdk.Stack):

    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Customer financial records are highly sensitive - require additional security controls
        if not self.node.try_get_context('is_financial_records'):
            raise ValueError("This stack is only for storing customer financial records")

        # Create a secure bucket with proper access controls
        bucket = s3.Bucket(
            self,
            "SecureFinancialRecordsBucket",
            bucket_name=f"financial-records-{cdk.Aws.RandomIdentifier()}",
            versioned=True,
            encryption=s3.BucketEncryption.KMS,
            block_public_access=s3.BlockPublicAccess(
                block_public_acls=True,
                block_public_policy=True,
                ignore_public_acls=True,
                restrict_public_buckets=True
            ),
            removal_policy=cdk.RemovalPolicy.DESTROY  # Secure deletion on stack removal
        )

        # Enable server-side encryption
        bucket.enable_server_side_encryption_by_default()

        # Enable versioning
        bucket.enable_versioning()

        # Enable logging to CloudWatch
        bucket.add_cors_rule(
            allowed_methods=[s3.HttpMethod.GET],
            allowed_origins=['*'],
            max_age_seconds=300
        )

        # Create a KMS key for encryption
        key = kms.Key(
            self,
            "SecureKey",
            enable_key_rotation=True,
            cross_region_key_enabled=True
        )

        # Attach key to bucket
        bucket.add_to_resource_policy(
            kms.CfnResourcePolicy(
                self,
                "KmsPolicy",
                resource=bucket.bucket_arn,
                statement=[
                    kms.CfnResourcePolicy.StatementProperty(
                        effect=kms.CfnResourcePolicy.StatementEffect.ALLOW,
                        principals=["*"],
                        actions=[
                            "s3:PutObject",
                            "s3:GetObject",
                            "s3:DeleteObject"
                        ],
                        resource=bucket.bucket_arn,
                        condition=kms.CfnResourcePolicy.ConditionProperty(
                            string_equals={
                                "s3:x-amz-server-side-encryption": "aws:kms"
                            }
                        )
                    )
                ]
            )
        )

        # Add logging to CloudWatch
        log_bucket = s3.Bucket(
            self,
            "FinancialRecordsLogs",
            bucket_name=f"financial-records-logs-{cdk.Aws.RandomIdentifier()}",
            versioned=True,
            block_public_access=s3.BlockPublicAccess.BLOCK_ALL,
            removal_policy=cdk.RemovalPolicy.DESTROY
        )

        # Configure bucket logging
        bucket.logging_config_property = s3.CfnBucket.LoggingConfigurationProperty(
            log_bucket=log_bucket.bucket_name,
            enabled=True
        )

        # Add deployment bucket for customer data
        deployment_bucket = s3deploy.BucketDeployment(
            self,
            "DeployFinancialRecords",
            sources=[s3deploy.Source.asset("./customer_data")],
            destination_bucket=bucket
        )