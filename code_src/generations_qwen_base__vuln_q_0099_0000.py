import aws_cdk as cdk

    from aws_cdk import (
        Stack,
        aws_s3 as s3
    )

    class S3BucketStack(Stack):

        def __init__(self, scope: cdk.Construct, id: str, **kwargs) -> None:
            super().__init__(scope, id, **kwargs)

            # Create an S3 bucket
            bucket = s3.Bucket(self, "MyBucket")

    app = cdk.App()
    S3BucketStack(app, "S3BucketStack")
    app.synth()

# ===== cell separator =====

import aws_cdk as cdk
from aws_cdk import (
    Stack,
    aws_s3 as s3
)

class S3BucketStack(Stack):

    def __init__(self, scope: cdk.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Create an S3 bucket
        bucket = s3.Bucket(self, "MyBucket",
            bucket_name="my-bucket-1234567890",  # You can use a custom bucket name
            removal_policy=cdk.RemovalPolicy.DESTROY,  # This will delete the bucket on stack destroy
            auto_delete_objects=True  # Automatically delete objects when the bucket is deleted
        )

        # Optionally, you can add some properties to the bucket
        bucket.public_access_block(
            block_public_acls=True,
            block_public_policy=True,
            ignore_public_acls=True,
            restrict_public_buckets=True
        )

        # Optionally, you can add some lifecycle rules
        bucket.add_lifecycle_rule(
            enabled=True,
            expiration_in_days=30,
            transition_to Glacier=True,
            storage_class=aws_s3.StorageClass.GLACIER
        )

app = cdk.App()
S3BucketStack(app, "S3BucketStack")
app.synth()