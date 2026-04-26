from aws_cdk import core
from aws_cdk import aws_s3 as s3

class MyCdkProjectStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Define the S3 bucket
        bucket = s3.Bucket(
            self, "MyCdkBucket",
            versioned=True,
            removal_policy=core.RemovalPolicy.DESTROY,  # Be careful with this in production
            auto_delete_objects=True  # Be careful with this in production
        )

app = core.App()
MyCdkProjectStack(app, "my-cdk-project")