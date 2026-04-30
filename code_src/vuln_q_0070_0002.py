import os
import logging
from aws_cdk.core import (
    aws_s3 as s3,
    aws_iam as iam,
    RemovalPolicy
)
from typing import Optional

class SecureS3Bucket:
    def __init__(self, 
                 name: str,
                 versioned: bool = True,
                 enforce_ssl: bool = True,
                 remove_pseudo_hostnames: bool = True,
                 public_read_access: bool = False):
        """
        Creates a secure S3 bucket with best practices.
        
        Args:
            name (str): The name of the bucket
            versioned (bool): Whether to enable versioning
            enforce_ssl (bool): Whether to enforce SSL
            remove_pseudo_hostnames (bool): Whether to remove pseudo-hostnames
            public_read_access (bool): Whether to allow public read access
        """
        # Validate inputs
        if not name or not isinstance(name, str):
            raise ValueError("Name must be a non-empty string")
            
        # Set up logging
        logging.basicConfig(level=logging.INFO)
        logger = logging.getLogger(__name__)
        
        # Get region from environment or default to us-east-1
        region = os.environ.get('AWS_DEFAULT_REGION', 'us-east-1')
        
        # Create the S3 bucket with secure defaults
        self.bucket = s3.Bucket(
            name,
            versioned=versioned,
            enforce_ssl=enforce_ssl,
            removal_policy=RemovalPolicy.DESTROY,  # Use RETAIN in production
            auto_delete_objects=True,
            versioned_s3_bucket=versioned,
            # Prevent public access by default
            public_read_access=public_read_access,
            # Remove potentially dangerous pseudo-hostnames
            remove_pseudo_hostnames=remove_pseudo_hostnames,
            # Enable logging
            logging=Logging(
                target=s3.LoggingTarget(
                    s3_logs_bucket_name=f"{name}-logs",
                    subject=f"{name}-logs"
                )
            ),
            # Enable VPC interface endpoint for secure access
            vpc_settings=s3.VpcSettings(
                subnet_mapping={
                    'SubnetType': s3.SubnetType.SUBNET_TYPE_VPC,
                    'SubnetIds': [  # Replace with actual subnet IDs
                        'subnet-12345678',
                        'subnet-87654321'
                    ]
                }
            )
        )
        
        # Create and attach the least privilege policy
        self.attach_iam_policy()
        
        logger.info(f"Created secure S3 bucket: {name}")

    def attach_iam_policy(self):
        """
        Attaches a least privilege IAM policy to the bucket.
        """
        # Create a new IAM role for the bucket
        role = iam.IAMRole(
            self.bucket,
            "S3AccessRole",
            assumed_by=iam.ServicePrincipal("s3.amazonaws.com")
        )
        
        # Create a policy with minimal permissions
        policy_document = {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Effect": "Allow",
                    "Action": [
                        "s3:GetObject",
                        "s3:ListBucket"
                    ],
                    "Resource": [
                        f"arn:aws:s3:::{self.bucket.name}",
                        f"arn:aws:s3:::{self.bucket.name}/*"
                    ]
                }
            ]
        }
        
        # Attach the policy to the role
        role.add_to_policy(
            iam.Policy(
                self, 
                f"{self.bucket.name}-policy",
                policy_document=policy_document
            )
        )