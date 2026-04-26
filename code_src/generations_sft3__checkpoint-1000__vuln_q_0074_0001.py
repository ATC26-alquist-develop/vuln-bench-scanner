from aws_cdk import core
from aws_cdk import aws_s3 as s3
from aws_cdk import aws_kms as kms
from aws_cdk import aws_s3_deployment as s3_deployment
from constructs import Construct

class SecureS3BucketStack(core.Stack):
    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Create a KMS key for encryption
        key = kms.Key(self, "SecureS3Key",
                      description="Secure S3 bucket encryption key",
                      enable_key_rotation=True)

        # Create an S3 bucket with encryption enabled
        bucket = s3.Bucket(self, "SecureS3Bucket",
                          encryption=s3.BucketEncryption.KMS,
                          encryption_key=key,
                          block_public_access=s3.BlockPublicAccess.BLOCK_ALL)

        # Deploy files to the bucket
        s3_deployment.BucketDeployment(self, "DeployFiles",
                                      sources=[s3_deployment.Source.asset("./sensitive_data")],
                                      destination_bucket=bucket)

app = core.App()
SecureS3BucketStack(app, "SecureS3BucketStack")
app.synth()