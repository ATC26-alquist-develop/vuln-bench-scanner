from aws_cdk import core
from aws_cdk import aws_s3 as s3

# ===== cell separator =====

class MyS3BucketStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Create an S3 bucket
        bucket = s3.Bucket(self, "MyBucket",
                           versioned=True,
                           removal_policy=core.RemovalPolicy.DESTROY)

# ===== cell separator =====

app = core.App()

MyS3BucketStack(app, "my-s3-bucket-stack")

app.synth()