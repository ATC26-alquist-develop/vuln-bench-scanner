import boto3
import logging
from typing import Optional
from aws_cdk import aws_s3 as s3
from aws_cdk import aws_kms as kms
from aws_cdk import core

class SecureS3BucketWithKMSKey(core.Construct):
    def __init__(self, scope: core.Construct, id: str, bucket_name: str, kms_key: Optional[kms.Key] = None):
        super().__init__(scope, id)
        
        # Configure logging
        logging.basicConfig(level=logging.INFO)
        logger = logging.getLogger(__name__)
        
        # Create S3 bucket with encryption
        self.bucket = s3.Bucket(
            self,
            bucket_name=bucket_name,
            encryption=s3.BucketEncryption.S3_MANAGED,
            # Enable server-side encryption by default
            server_side_encryption_configuration=s3.ServerSideEncryptionConfiguration(
                rules=[
                    s3.ServerSideEncryptionApplyRule(
                        apply_server_side_encryption_by_default=True,
                        sse_algorithm=s3.ServerSideEncryptionAlgorithm.SSE_S3_MANAGED
                    )
                ]
            )
        )
        
        # Add KMS key if provided
        if kms_key:
            self.bucket.add_server_side_encryption(
                rules=[
                    s3.ServerSideEncryptionApplyRule(
                        apply_server_side_encryption_by_default=True,
                        sse_algorithm=s3.ServerSideEncryptionAlgorithm.SSE_KMS,
                        kms_master_key=s3.KmsKey.from_key(kms_key)
                    )
                ]
            )
        
        # Log bucket creation
        logger.info(f"Created bucket {bucket_name} with encryption")
        
        # Add bucket policy (example - adjust as needed)
        self.bucket.add_to_resource_policy(
            s3.BucketPolicy(
                self,
                bucket=bucket_name,
                policy_document={
                    "Version": "2012-10-17",
                    "Statement": [
                        {
                            "Effect": "Allow",
                            "Principal": "*",
                            "Action": "s3:GetObject",
                            "Resource": f"arn:aws:s3:::{bucket_name}/*",
                            "Condition": {
                                "StringEquals": {
                                    "s3:ExistingObjectTag/Owner": "your-organization"
                                }
                            }
                        }
                    ]
                }
            )
        )
        
        # Log policy addition
        logger.info(f"Added bucket policy to {bucket_name}")

def main(app, context):
    # Example usage
    kms_key = kms.Key.from_key_id(
        "arn:aws:kms:us-west-2:123456789012:key/1234abcd-12ab-34cd-56ef-1234567890ab"
    )
    bucket = SecureS3BucketWithKMSKey(
        scope=app,
        id="secure_bucket",
        bucket_name="my-secure-bucket",
        kms_key=kms_key
    )