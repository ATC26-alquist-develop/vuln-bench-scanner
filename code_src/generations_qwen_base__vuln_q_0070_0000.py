from aws_cdk import core as cdk
from aws_cdk import aws_s3 as s3

class MyS3Stack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Create an S3 bucket
        bucket = s3.Bucket(self, "MyS3Bucket")

app = cdk.App()
MyS3Stack(app, "MyS3Stack")
app.synth()

# ===== cell separator =====

class MyS3Stack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Create an S3 bucket with a lifecycle policy
        bucket = s3.Bucket(self, "MyS3Bucket",
                           bucket_name="my-bucket",
                           removal_policy=cdk.RemovalPolicy.DESTROY,
                           lifecycle_rules=[
                               s3.LifecycleRule(
                                   enabled=True,
                                   rule_type=s3.LifecycleRuleType.AFTER_MOST_RECENT,
                                   abort_incomplete_multipart_upload_after=cdk.Duration.days(7),
                                   expiration_after=cdk.Duration.days(30),
                                   noncurrent_version_expiration_after=cdk.Duration.days(60),
                                   noncurrent_version_transition_after=cdk.Duration.days(90),
                               )
                           ])

app = cdk.App()
MyS3Stack(app, "MyS3Stack")
app.synth()