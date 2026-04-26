# Import the necessary CDK modules

from aws_cdk import core

from aws_cdk import aws_s3 as s3


# Define your CDK app

app = core.App()


# Define your stack

stack = core.Stack(app, "s3-bucket-stack")


# Define the S3 bucket

bucket = s3.Bucket(stack, "MyUniqueBucketName", 


    # Set the bucket properties

    versioned=True, 


    # Set the bucket to be publicly readable (be cautious with this)

    public_read=True, 


    # Set the bucket to be private by default

    removal_policy=core.RemovalPolicy.DESTROY,  # Be careful with this in production


    # Set the bucket to be encrypted

    encryption=s3.BucketEncryption.S3_MANAGED


    # Set the bucket to be hosted on a specific region

    location=s3.Region.US_EAST_1


    # Set the bucket to have a lifecycle rule

    lifecycle_rule=core.LifecycleRule(stack, "MyLifecycleRule", 


        # Transition objects to Glacier after 30 days

        transition=core.LifecycleTransition(day=30, storage_class="GLACIER"),

        # Delete objects after 365 days

        expiration=core.Duration.days(365))

)


# Synthesize the stack to generate the CloudFormation template

app.synth()