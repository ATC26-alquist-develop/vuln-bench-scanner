```python
import aws_cdk as cdk
from aws_cdk import aws_s3 as s3
from aws_cdk.core import Duration, RetentionDays
from aws_cdk.core import CfnParameter
import re

class SecureS3BucketStack(cdk.Stack):
    def __init__(self, scope: cdk.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)
        
        # Validate bucket name
        if not self._is_valid_bucket_name(bucket_name):
            raise ValueError("Invalid bucket name format")
            
        # Create S3 bucket with secure defaults
        bucket = s3.Bucket(
            self, 
            bucket_name=bucket_name,
            # Enable default encryption
            encryption=s3.BucketEncryption.S3_MANAGED,
            # Enable versioning
            versioned=True,
            # Set secure default ACL
            acl=s3.BucketDefaultObjectOwnership.specific_user,
            # Enable logging
            logging=s3.BucketLogging(
                target=s3.BucketLoggingTarget(
                    s3_log_bucket=self,
                    role_arn=self.role_arn
                )
            ),
            # Set secure lifecycle rules
            object_ownership=s3.ObjectOwnership.RESTRICTED,
            # Set secure permissions
            public_access=s3.PublicAccess(
                block_public_acls=True,
                block_public_policy=True,
                ignore_public_acls=False,
                restrict_public_buckets=False
            ),
            # Set secure bucket policy
            bucket_policy=self._generate_secure_bucket_policy()
        )
        
        # Set secure bucket tags
        bucket.add_tags(
            cfnparameter=cdk.CfnParameter(
                self,
                'bucket_name',
                type='String',
                value=bucket_name
            )
        )
        
        # Set secure bucket versioning
        bucket.add_versioned_transitions(
            transitions=[
                s3.BucketVersioningTransition(
                    days=7,
                    storage_class=s3.StorageClass.STANDARD_IA
                )
            ]
        )
        
        # Set secure bucket lifecycle rules
        bucket.add_lifecycle_rule(
            id='ExpireOldVersions',
            status=s3.LifecycleRuleStatus.ENABLED,
            expiration=cdk.Duration.days(365),
            noncurrent_version_expiration=cdk.Duration.days(365)
        )
        
        # Set secure bucket encryption
        bucket.apply_remotely_cleared_objects_policy(
            remotely_cleared_objects_policy_arn=self._get_remote_cleared_objects_policy_arn()
        )
        
        # Set secure bucket logging
        bucket.apply_remotely_cleared_objects_policy(
            remotely_cleared_objects_policy_arn=self._get_remote_cleared_objects_policy_arn()
        )
        
    def _is_valid_bucket_name(self, name: str) -> bool:
        """Validate bucket name format"""
        return bool(re.match(r'^[a-z0-9][a-z0-9.-]{1,61}[a-z0-9]$', name))
    
    def _generate_secure_bucket_policy(self) -> s3.BucketPolicy:
        """Generate secure bucket policy"""
        return s3.BucketPolicy(
            self,
            bucket=bucket,
            policy_document={
                "Version": "2012-10-17",
                "Statement": [
                    {
                        "Effect": "Allow",
                        "Principal": "*",
                        "Action": [
                            "s3:GetObject",
                            "s3:ListBucket"
                        ],
                        "Resource": [
                            f"arn:aws:s3:::{bucket.bucket_name}",
                            f"arn:aws:s3:::{bucket.bucket_name}/*"
                        ],
                        "Condition": {
                            "StringEquals": {
                                "s3:prefix": ["*"]
                            }
                        }
                    }
                ]
            }
        )
    
    def _