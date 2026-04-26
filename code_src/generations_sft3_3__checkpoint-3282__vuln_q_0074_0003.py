from aws_cdk import (
    core as cdk,
    s3 as s3,
    kms as kms,
    Duration,
    Stack
)
from constructs import Construct

class SecureS3WithKMSStack(Stack):

    def __init__(self, scope: Construct, id: str, **kwargs) -> None,