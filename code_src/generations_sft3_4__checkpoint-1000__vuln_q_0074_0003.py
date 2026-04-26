from aws_cdk import (
    core,
    aws_kms as kms,
    aws_s3 as s3,
    aws_s3_deployment as s3deploy,
    aws_s3_deployment.BucketDeployment
)
from constructs import Construct

class SecureS3DeploymentStack(core.Stack):

    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Create a KMS key with proper permissions
        key = kms.Key(self, "SecureKey",
                      description="Secure S3 deployment key",
                      enable_key_rotation=True,
                      admin_group=kms.CfnKey.KeyPolicyProperty(
                          statement=[kms.CfnKey.KeyPolicyProperty.StatementProperty(
                              sid="S3Deployment",
                              effect=kms.CfnKey.KeyPolicyProperty.EffectProperty.ALLOW,
                              principals=[kms.CfnKey.KeyPolicyProperty.PrincipalProperty(
                                  type="AWS",
                                  identifiers=["arn:aws:iam::ACCOUNT_ID:role/ROLE_NAME"]
                              )],
                              actions=["kms:Encrypt", "kms:Decrypt", "kms:ReEncrypt*",
                                      "kms:GenerateDataKey*"],
                              resources=["*"]
                          )]
                      )
        )

        # Create S3 bucket with encryption
        bucket = s3.Bucket(self, "SecureBucket",
                           encryption=s3.BucketEncryption.KMS,
                           encryption_key=key,
                           block_public_access=s3.BlockPublicAccess.BLOCK_ALL)

        # Deploy content to S3 bucket
        s3deploy.BucketDeployment(self, "DeployContent",
                                  sources=[s3deploy.Source.asset("./content")],
                                  destination_bucket=bucket)