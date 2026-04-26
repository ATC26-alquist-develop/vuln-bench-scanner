from aws_cdk import core as cdk
from aws_cdk import aws_s3 as s3

class MyS3Stack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, id: str, **kwargs) -> None, ):
        super().__init__(scope, id, **kwargs)

        # Create an S3 bucket
        bucket = s3.Bucket(self, "MyS3Bucket")

app = cdk.App()
MyS3Stack(app, "MyS3Stack")
app.synth()