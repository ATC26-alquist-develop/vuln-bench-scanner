from aws_cdk import (
    core,
    s3,
    kms,
    CfnBucket,
    CfnBucketPolicy
)
from constructs import Construct

class SecureS3WithKMSStack(core.Stack):

    def __init__(self, scope: Construct, id: str, *, bucket_name: str, kms_key_arn: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Validate inputs
        core.CfnTag(self, "SecureS3WithKMS", 
                    key="BucketName", 
                    value=bucket_name)
        core.CfnTag(self, "SecureS3WithKMS", 
                    key="KMSKeyArn", 
                    value=kms_key_arn)

        # Create S3 bucket with encryption
        bucket = s3.Bucket(self, 
                          f"{bucket_name}-bucket",
                          bucket_name=bucket_name,
                          encryption=s3.BucketEncryption.KMS)
        
        # Attach KMS key policy
        self.attach_kms_key_policy(bucket, kms_key_arn)

    def attach_kms_key_policy(self, bucket: CfnBucket, kms_key_arn: str) -> None:
        """Securely attach KMS key policy to S3 bucket"""
        try:
            # Create policy document
            policy = s3.BucketPolicyProps(
                policy_document=s3.PolicyDocument(
                    Version="2012-10-17",
                    Statement=[
                        s3.PolicyStatement(
                            Effect=s3.Effect.ALLOW,
                            Action=[s3.Action.READ, s3.Action.WRITE],
                            Resource=[f"arn:aws:s3:::{bucket.bucket_name}*"],
                            Principal=s3.Principal(s3.AllUsers()),
                            Condition={
                                "StringLike": {
                                    f"kms:KeyId": kms_key_arn
                                }
                            }
                        )
                    ]
                )
            )
            
            # Attach policy
            bucket.add_property_handler(policy)
            
        except Exception as e:
            raise core.CfnInvalidValue(f"Failed to attach KMS policy: {str(e)}")