from aws_cdk import core
import re

class SecureS3Bucket(core.Construct):
    def __init__(self, scope: core.Construct, id: str, bucket_name: str, **kwargs):
        super().__init__(scope, id)
        
        # Validate bucket name
        if not self._is_valid_bucket_name(bucket_name):
            raise ValueError("Invalid bucket name format")
            
        # Create S3 bucket with default security settings
        self.bucket = core.aws_s3.Bucket(
            self,
            id=id,
            bucket_name=bucket_name,
            **kwargs
        )
        
    def _is_valid_bucket_name(self, name: str) -> bool:
        """Validate S3 bucket name format and restrictions"""
        # Bucket name must be 3-63 chars, lowercase, and can only contain:
        # - lowercase letters, numbers, dots, hyphens, and underscores
        # - cannot start or end with a dot
        # - cannot contain consecutive dots
        if not isinstance(name, str):
            return False
            
        if not 3 <= len(name) <= 63:
            return False
            
        if name.startswith('.') or name.endswith('.') or '..' in name:
            return False
            
        if not re.match(r'^[a-z0-9][a-z0-9.-]{1,61}[a-z0-9]$', name):
            return False
            
        return True