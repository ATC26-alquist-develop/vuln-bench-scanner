from aws_cdk import (
    core,
    aws_kms as kms,
    aws_s3 as s3,
    aws_s3_deployment as s3deploy,
    aws_s3_assets as assets,
    aws_s3_deployment as s3deploy
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
                                       "kms:GenerateDataKey*", "kms:DescribeKey"],
                              resources=["*"]
                          )]
                      ))

        # Create a secure S3 bucket
        bucket = s3.Bucket(self, "SecureBucket",
                          encryption=s3.BucketEncryption.KMS,
                          encryption_key=key,
                          block_public_access=s3.BlockPublicAccess.BLOCK_ALL)

        # Create a secure deployment
        with assets.Asset(self, "SecureAssets",
                         path="./secure-assets") as asset:
            s3deploy.BucketDeployment(self, "DeployAssets",
                                     sources=[s3deploy.Source.asset(asset.path)],
                                     destination_bucket=bucket)