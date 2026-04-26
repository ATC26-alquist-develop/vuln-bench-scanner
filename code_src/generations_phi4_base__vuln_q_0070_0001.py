# Import the required CDK modules

from aws_cdk import core as cdk

from aws_cdk import aws_s3 as s3


class MyWebAppBucketStack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, id: str, **kwargs) -> None:

        super().__init__(scope, id, **kwargs)

        # Create an S3 bucket with public read access

        bucket = s3.Bucket(self, "MyWebAppBucket",

                           versioned=True,

                           encryption=s3.BucketEncryption.S3_MANAGED,

                           public_read_access=True)


app = cdk.App()

MyWebAppBucketStack(app, "MyWebAppBucketStack")

app.synth()