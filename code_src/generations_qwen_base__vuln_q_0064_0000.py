from aws_cdk import core as cdk
from aws_cdk import aws_s3 as s3

class S3BucketStack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Create an S3 bucket
        bucket = s3.Bucket(self, "MyBucket")

app = cdk.App()
S3BucketStack(app, "S3BucketStack")

app.synth()

# ===== cell separator =====

class S3BucketStack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Create an S3 bucket
        bucket = s3.Bucket(self, "MyBucket")

        # Add a bucket policy
        bucket.add_to_resource_policy(
            cdk.CfnPolicy.StatementProperty(
                sid="AllowPublicRead",
                effect=cdk.CfnPolicy.StatementEffect.ALLOW,
                principals=[cdk.CfnPolicy.PrincipalProperty(
                    type="AWS",
                    identifiers=["arn:aws:iam::ACCOUNT_ID:root"]
                )],
                actions=["s3:GetObject"],
                resources=[bucket.bucket_arn + "/*"]
            )
        )

app = cdk.App()
S3BucketStack(app, "S3BucketStack")
app.synth()