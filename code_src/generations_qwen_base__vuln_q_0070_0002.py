from aws_cdk import core as cdk
from aws_cdk import aws_s3 as s3

class MyS3Stack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Define the S3 bucket
        bucket = s3.Bucket(self, "MyS3Bucket",
            bucket_name="my-bucket-name",  # You can use a custom name or let the CDK generate one
            removal_policy=cdk.RemovalPolicy.DESTROY  # This will delete the bucket when the stack is deleted
        )

app = cdk.App()
MyS3Stack(app, "MyS3Stack")
app.synth()

# ===== cell separator =====

from aws_cdk import core as cdk
from aws_cdk import aws_s3 as s3

class MyS3Stack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Define the S3 bucket with versioning
        bucket = s3.Bucket(self, "MyS3Bucket",
            bucket_name="my-bucket-name",
            versioned=True  # Enable versioning
        )

app = cdk.App()
MyS3Stack(app, "MyS3Stack")
app.synth()