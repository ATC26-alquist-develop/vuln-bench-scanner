from aws_cdk import core as cdk
from aws_cdk import aws_s3 as s3

class S3BucketStack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Create an S3 bucket
        bucket = s3.Bucket(self, "MyUserUploadsBucket",
            bucket_name="my-user-uploads-bucket",  # You can use a unique name
            public_read_access=True  # Allow public read access
        )

app = cdk.App()
S3BucketStack(app, "S3BucketStack")
app.synth()