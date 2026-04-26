from aws_cdk import core as cdk
from aws_cdk import aws_s3 as s3
from aws_cdk import aws_s3_deployment as s3deploy
from aws_cdk import aws_kms as kms
from constructs import Construct

class SecureS3BucketStack(cdk.Stack):

    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Create a secure bucket with encryption
        bucket = s3.Bucket(
            self,
            "SecureBucket",
            bucket_name=f"secure-bucket-{cdk.Aws.RandomValueGenerator.generate().string(8)}",
            encryption=s3.BucketEncryption.KMS_MANAGED,
            versioned=True,
            removal_policy=cdk.RemovalPolicy.DESTROY
        )

        # Create a key for encryption
        key = kms.Key(
            self,
            "SecureKey",
            enable_key_rotation=True,
            admin_group=["system:masters"]
        )

        # Deploy objects with encryption
        s3deploy.BucketDeployment(
            self,
            "DeployObjects",
            sources=[s3deploy.Source.asset("./content")],
            destination_bucket=bucket,
            encryption_key=key
        )

        # Add logging
        cdk.CfnOutput(self, "BucketName", value=bucket.bucket_name)
        cdk.CfnOutput(self, "EncryptionKeyArn", value=key.key_arn)