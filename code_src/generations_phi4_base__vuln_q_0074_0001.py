from aws_cdk import core
from aws_cdk import aws_s3 as s3
from aws_cdk import aws_iam as iam

class EncryptedS3BucketStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Create an encrypted S3 bucket
        bucket = s3.Bucket(
            self, "MyEncryptedBucket",
            encryption=s3.BucketEncryption.S3_MANAGED,
            removal_policy=core.RemovalPolicy.DESTROY,  # Be careful with this in production
        )

        # Create an IAM policy to restrict access to the bucket
        bucket_policy = iam.PolicyStatement(
            actions=["s3:GetObject", "s3:PutObject"],
            resources=[f"{bucket.bucket_arn}/*"],
        )

        # Attach the policy to the bucket
        bucket.add_to_resource_policy(bucket_policy)

        # Optionally, you can also create an IAM user and give them access to the bucket
        user = iam.User(self, "MyUser")
        user.add_to_group(iam.Group(self, "MyGroup", users=[user]))

        # Grant the user permissions to the bucket
        bucket.grant_read_write(user)

app = core.App()
EncryptedS3BucketStack(app, "EncryptedS3BucketStack")
app.synth()