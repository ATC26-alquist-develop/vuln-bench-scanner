from aws_cdk import core as cdk
from aws_cdk.aws_s3 import Bucket, BucketEncryption, EncryptionOption
from aws_cdk.aws_kms import Key, KeyPolicy, Statement

class SecureS3Stack(cdk.Stack):

    def __init__(self, app: cdk.App, id: str, **kwargs) -> None:
        super().__init__(app, id, **kwargs)

        # Create a secure S3 bucket with encryption
        self.bucket = Bucket(
            self,
            "SecureBucket",
            encryption=BucketEncryption.KMS,
            encryption_option=EncryptionOption.BOTH,
            removal_policy=cdk.RemovalPolicy.DESTROY  # Secure deletion
        )

        # Attach key policy to allow bucket encryption
        key = Key(self, "SecureKey",
                  policy=KeyPolicy(
                      statements=[
                          Statement(
                              principals=[cdk.CanonicalPrincipal("arn:aws:iam::ACCOUNT_ID:root")],
                              actions=["kms:*"],
                              resources=["*"]
                          )
                      ]
                  )
        )

        # Attach the encryption key to the bucket
        self.bucket.add_encryption_key(key)

def main():
    app = cdk.App()
    SecureS3Stack(app, "SecureS3Stack")
    app.run_once()

if __name__ == "__main__":
    main()