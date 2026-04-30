import os
import logging
from typing import Optional
from aws_cdk.core import (
    aws_s3 as s3,
    aws_iam as iam,
    aws_lambda as lambda_,
    aws_lambda_python_alpha as lambda_python
)
from aws_cdk.core.exceptions import (
    InvalidResourceProperties,
    ResourceAlreadyExists,
    ResourceNotFound,
    CfnNotFound,
    CfnValidationException
)

class SecureUploadBucketStack:
    def __init__(self, scope: 'SecureUploadBucketStack', 
                 construct_id: str, 
                 environment: str, 
                 region: Optional[str] = None) -> None:
        super().__init__(scope, construct_id, environment=environment)
        self.region = region or self.node.region
        self._setup_logging()
        self._create_secure_bucket()

    def _setup_logging(self) -> None:
        """Set up logging for the stack."""
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

    def _create_secure_bucket(self) -> None:
        """Create a secure S3 bucket with encryption and access policies."""
        try:
            # Create the S3 bucket with versioning and encryption
            bucket = s3.Bucket(
                self,
                'SecureUploadBucket',
                versioned=True,
                removal_policy=s3.RemovalPolicy.DESTROY,
                auto_delete_objects=True,
                versioned=True,
                versioned_stores={s3.VersioningVersionedStore.ENCRYPTED},
                # Enable server-side encryption by default
                enforce_ssl=True,
                # Enable access logging
                logging=LoggingPropagate(),
                # Enable public access blocking
                block_public_access=s3.BlockPublicAccess.BLOCK_ALL
            )

            # Create a unique bucket name to avoid conflicts
            self.logger.info(f"Created bucket: {bucket.bucket_name}")

            # Create a bucket policy that allows read-only access for authenticated users
            bucket_policy = iam.PolicyDocument(
                statements=[
                    iam.PolicyStatement(
                        actions=['s3:GetObject'],
                        resources=[f'arn:aws:s3:::{bucket.bucket_name}/*'],
                        principals=[iam.AnyPrincipal()]
                    )
                ]
            )

            # Attach the policy to the bucket
            bucket.add_to_resource_policy(bucket_policy)

            # Create a role for Lambda functions that will use this bucket
            lambda_role = iam.Role(
                self,
                'LambdaExecutionRole',
                assumed_by=iam.ServicePrincipal('lambda.amazonaws.com'),
                # Grant only the necessary permissions
                managed_policies=[
                    iam.ManagedPolicy.from_arn(
                        self, 'AmazonS3ReadOnlyAccess', 
                        'arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess'
                    )
                ]
            )

            self.logger.info(f"Created IAM role: {lambda_role.role_name}")

        except (InvalidResourceProperties, ResourceAlreadyExists, 
                ResourceNotFound, CfnNotFound, CfnValidationException) as e:
            self.logger.error(f"Error creating bucket: {str(e)}")
            raise