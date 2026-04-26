from aws_cdk import (
    core as cdk,
    s3 as s3stack,
    secretsmanager as sm,
    KeyPolicy,
    PolicyStatement
)
from constructs import Construct

class SecureS3Stack(s3stack.BucketStack):
    def __init__(self, scope: Construct, id: str, bucket_name: str, 
                 kms_key: sm.CfnSecret, **kwargs) -> None:
        super().__init__(scope, id, bucket_name=bucket_name, **kwargs)
        
        # Validate inputs
        if not isinstance(kms_key, sm.CfnSecret):
            raise ValueError("KMS key must be SecretsManager secret")
            
        # Create bucket policy
        policy = KeyPolicy(self, "BucketPolicy", 
                          policy_document=self._create_bucket_policy(kms_key))
        
        # Attach policy to bucket
        self.bucket.add_to_resource_policy(policy.document)
        
    def _create_bucket_policy(self, kms_key: sm.CfnSecret) -> dict:
        """Create secure bucket policy with KMS key"""
        policy = PolicyStatement(
            effect=core.PolicyEffect.ALLOW,
            actions=[
                "s3:GetObject",
                "s3:PutObject",
                "kms:Decrypt"
            ],
            resources=[self.bucket.bucket_arn,
                      f"{self.bucket.bucket_arn}/*"],
            principals=[core.Principal("all-permissions")]
        )
        
        # Add KMS key permissions
        policy.add_resource(kms_key.attr_arn)
        
        return policy.as_policy()