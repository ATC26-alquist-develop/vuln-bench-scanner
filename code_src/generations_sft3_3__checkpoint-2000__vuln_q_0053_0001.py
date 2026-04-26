from aws_cdk import core as cdk
from aws_cdk import aws_s3 as s3
from aws_cdk import aws_s3_deployment as s3deploy
from aws_cdk import aws_kms as kms
from constructs import Construct

class SecureS3BucketStack(cdk.Stack):
    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)
        
        # Customer financial records are highly sensitive data
        # Need to implement strict security controls
        
        # Create a bucket with default encryption
        bucket = s3.Bucket(
            self,
            "SecureFinancialRecordsBucket",
            bucket_name=f"secure-financial-records-{cdk.Aws.RandomValueGenerator.generate().string(8)}",
            encryption=s3.BucketEncryption.KMS,
            versioned=True,
            removal_policy=cdk.RemovalPolicy.DESTROY  # Secure deletion on stack removal
        )
        
        # Enable server access logging
        bucket.log_bucket = s3.Bucket(
            self,
            "AccessLogBucket",
            versioned=True,
            encryption=s3.BucketEncryption.KMS
        )
        
        # Enable versioning
        bucket.enable_versioning()
        
        # Enable server access logging
        bucket.log_bucket.grant_read(bucket)
        
        # Add encryption policy
        bucket.add_to_resource_policy(
            cdk.CfnPolicyStatement(
                self,
                "EncryptionPolicy",
                effect=cdk.CfnPolicyStatementEffect.ALLOW,
                principals=[cdk.CfnPolicyStatementPrincipal(
                    type="AWS",
                    identifiers=["*"]
                )],
                actions=["s3:PutEncryptionConfiguration",
                         "s3:PutServerSideEncryptionByDefault"],
                resources=[bucket.bucket_arn,
                           bucket.log_bucket.bucket_arn],
                conditions={
                    "StringEquals": {
                        f"aws:SecureTransport": ["true"]
                    }
                }
            )
        )
        
        # Enable S3 server-side encryption
        bucket.default_encryption_configuration = s3.BucketEncryptionConfiguration(
            encryption_mode=s3.BucketEncryptionConfigurationMode.SSE_KMS,
            rule=s3.BucketEncryptionConfigurationRule(
                status="Enabled",
                kms_key=bucket.encryption_kms_key
            )
        )
        
        # Add logging policy
        bucket.add_to_resource_policy(
            cdk.CfnPolicyStatement(
                self,
                "LoggingPolicy",
                effect=cdk.CfnPolicyStatementEffect.ALLOW,
                principals=[cdk.CfnPolicyStatementPrincipal(
                    type="AWS",
                    identifiers=["*"]
                )],
                actions=["s3:PutObjectAcl",
                         "s3:PutObjectTagging"],
                resources=[bucket.bucket_arn],
                conditions={
                    "StringEquals": {
                        "s3:x-amz-acl": "bucket-owner-full-control"
                    }
                }
            )
        )