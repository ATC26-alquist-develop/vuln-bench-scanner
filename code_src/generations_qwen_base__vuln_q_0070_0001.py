from aws_cdk import core as cdk
from aws_cdk import aws_s3 as s3

class WebAppS3BucketStack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Create an S3 bucket
        bucket = s3.Bucket(self, "WebAppBucket",
                           bucket_name="my-webapp-bucket",
                           public_read_access=True,
                           block_public_access=s3.BlockPublicAccess(
                               blocks_public_acls=True,
                               blocks_public_policy=True,
                               restrict_public_buckets=True
                           )
        )

app = cdk.App()
WebAppS3BucketStack(app, "WebAppS3BucketStack")
app.synth()