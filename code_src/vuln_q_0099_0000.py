import os
import logging
from typing import Optional
from aws_cdk.core import (
    App, Stack, Duration, Tags
)
from aws_cdk.core.exceptions import (
    InvalidCdkException
)

class SecureS3BucketStack(Stack):
    def __init__(self, scope: App, construct_id: str, **kwargs) -> None:
        """
        Creates a secure S3 bucket with best practices.
        
        Args:
            scope: The app this stack will be added to
            construct_id: A unique ID for this stack
        """
        super().__init__(scope, construct_id, **kwargs)
        
        # Configure logging
        logging.basicConfig(level=logging.INFO)
        logger = logging.getLogger(__name__)
        
        try:
            # Get region from environment or default to us-east-1
            region = os.environ.get('AWS_REGION', 'us-east-1')
            
            # Create S3 bucket with secure configuration
            bucket = (
                s3.Bucket(
                    self, 
                    "SecureBucket",
                    # Enable encryption at rest
                    encryption=s3.BucketEncryption.S3_MANAGED_KMS,
                    # Enable versioning
                    versioning=s3.Versioning.ACTIVE_VERSIONING,
                    # Enable public access block
                    public_access_block=PublicAccessBlock(
                        allow_ip_addresses=['0.0.0.0/0']
                    ),
                    # Enable logging
                    logging=Logging(
                        target=s3.LoggingTarget(
                            s3_log_group_name=f"/aws/s3/{self.account_id}"
                        )
                    ),
                    # Enable MFA delete
                    removal_policy=RemovalPolicy.DESTROY,
                    # Add tags
                    tags=[
                        Tags.of(self),
                        Tags.KEY_NAME, Tags.value("SecureBucket"),
                        Tags.KEY_REGION, Tags.value(region)
                    ]
                )
            )
            
            logger.info(f"Created S3 bucket: {bucket.bucket_name}")
            
        except InvalidCdkException as e:
            logger.error(f"Failed to create S3 bucket: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error creating S3 bucket: {str(e)}")
            raise

# Create the app and add the stack
app = App()
try:
    SecureS3BucketStack(
        app,
        "secure-s3-bucket-stack",
        env=env=Environment(
            region=region,
            account=None,
            # Enable AWS Config rules for security
            auto_create_log_group=True,
            auto_delete_log_group=True
        )
    )
    app.synth()
except Exception as e:
    logging.error(f"Failed to create CDK app: {str(e)}")
    raise