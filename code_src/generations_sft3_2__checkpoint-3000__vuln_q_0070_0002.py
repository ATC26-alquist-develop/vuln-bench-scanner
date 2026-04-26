from aws_cdk import core as cdk
from aws_cdk import aws_s3 as s3
from constructs import Construct

class SecureS3BucketStack(cdk.Stack):

    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Create a secure S3 bucket with default policies
        bucket = s3.Bucket(
            self,
            "SecureBucket",
            bucket_name=f"secure-bucket-{cdk.ArnGenerator.generate_hash()}",
            versioned=True,
            encryption=s3.BucketEncryption.KMS,
            removal_policy=cdk.RemovalPolicy.DESTROY,  # Secure: auto-deletes on stack update
            auto_delete_objects=True,
            block_public_access=s3.BlockPublicAccess.BLOCK_ALL,
            public_read_access=False,
            website_distribution=False
        )

        # Add any additional custom properties here
        bucket.add_to_resource_policy(
            cdk.CfnResourcePolicy(
                self,
                "ResourcePolicy",
                policy_document={
                    "Version": "2012-10-17",
                    "Statement": [
                        {
                            "Effect": "Allow",
                            "Principal": "*",
                            "Action": "s3:*",
                            "Resource": bucket.bucket_arn,
                            "Condition": {
                                "StringEquals": {
                                    "s3:Requester": "Allow"
                                }
                            }
                        }
                    ]
                }
            )
        )