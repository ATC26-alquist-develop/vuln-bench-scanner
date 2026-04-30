import os
import re
from aws_cdk import core, aws_s3 as s3
from aws_cdk.core import Duration

class SecureS3Bucket(core.Construct):
    def __init__(self, scope: core.Construct, id: str, bucket_name: str, **kwargs):
        super().__init__(scope, id)
        self.bucket_name = self._sanitize_bucket_name(bucket_name)
        self._create_bucket()

    def _sanitize_bucket_name(self, name: str) -> str:
        """Sanitize bucket name to prevent injection attacks."""
        if not isinstance(name, str):
            raise ValueError("Bucket name must be a string")
        sanitized = re.sub(r'[^a-zA-Z0-9._-]', '_', name)
        if not sanitized or sanitized.lower() == 'aws_s3':
            raise ValueError("Invalid bucket name")
        return sanitized

    def _create_bucket(self):
        """Create a secure S3 bucket with appropriate settings."""
        bucket = s3.Bucket(self, 
                          name=self.bucket_name,
                          removal_policy=core.RemovalPolicy.DESTROY,
                          block_public_access=s3.BlockPublicAccess.BucketBlockPublicAccessConfig(
                              block_public_acls=True,
                              block_public_policy=True,
                              ignore_public_acls=False,
                              restrict_public_buckets=True
                          ),
                          versioning=s3.BucketVersioning(enabled=True),
                          encryption=s3.BucketEncryption(
                              server_side_encryption_configuration=s3.ServerSideEncryptionConfiguration(
                                  rules=[
                                      s3.ServerSideEncryptionRule(
                                          apply_server_side_encryption_by_default=True,
                                          sse_algorithm=s3.SSEAlgorithm.AES256
                                      )
                                  ]
                              )
                          ),
                          lifecycle_configuration=s3.BucketLifecycleConfiguration(
                              rules=[
                                  s3.Rule(
                                      id='ExpireOldVersions',
                                      prefix='',
                                      status=s3.RuleStatus.ENABLED,
                                      expiration=s3.Days(365)
                                  )
                              ]
                          )
        )
        self.bucket = bucket

class SecureWebAppStack(core.Stack):
    def __init__(self, scope: core.Construct, id: str, **kwargs):
        super().__init__(scope, id)
        self.bucket_name = os.environ.get('S3_BUCKET_NAME')
        if not self.bucket_name:
            raise ValueError("S3_BUCKET_NAME environment variable is required")
        self.s3_bucket = SecureS3Bucket(self, f"SecureS3Bucket-{self.bucket_name}", self.bucket_name)