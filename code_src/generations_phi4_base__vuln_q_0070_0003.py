from aws_cdk import core
from aws_cdk import aws_s3 as s3

# ===== cell separator =====

class UserUploadsBucketStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Create an S3 bucket for user uploads
        user_uploads_bucket = s3.Bucket(
            self,
            "UserUploadsBucket",
            versioned=True,
            removal_policy=core.RemovalPolicy.DESTROY,  # Be cautious with this in production
            auto_delete_objects=True,  # Automatically delete objects when the bucket is deleted
            public_read_access=False,  # Set to True if you want the bucket to be publicly readable
            encryption=s3.BucketEncryption.S3_MANAGED,
            block_public_acls=True,
            block_public_policy=True,
            ignore_public_acls=True,
            restrict_public_buckets=True
        )

        # Output the bucket name
        core.CfnOutput(self, "BucketName", value=user_uploads_bucket.bucket_name)

# Define the app and stack
app = core.App()
UserUploadsBucketStack(app, "UserUploadsBucketStack")
app.synth()