from aws_cdk import (
    aws_s3 as s3,
    aws_kms as kms,
    core
)

class SecureS3BucketWithKMSKey(core.Construct):
    def __init__(self, scope: core.Construct, id: str, **kwargs):
        super().__init__(scope, id, **kwargs)
        
        # Create a KMS key
        key = kms.Key(self, "S3Key",
                     enable_key_rotation=True,
                     description="Key for S3 bucket encryption",
                     removal_policy=core.RemovalPolicy.RETAIN)
        
        # Create S3 bucket with server-side encryption
        bucket = s3.Bucket(self, "SecureBucket",
                          encryption=s3.BucketEncryption.KMS,
                          encryption_key=key,
                          block_public_acls=True,
                          block_public_policy=True,
                          enforce_ssl=True,
                          versioned=True,
                          lifecycle_rules=[
                              s3.LifecycleRule(
                                  noncurrent_version_expiration=s3.NoncurrentVersionExpiration(days=30)
                              )
                          ],
                          logging=core.ProtectLogGroup,
                          versioned=True)