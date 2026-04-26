To create an S3 bucket using AWS CDK and encrypt its contents, you can follow these steps:

1. Install the necessary dependencies:
   ```
   npm install aws-cdk @aws-cdk/aws-s3 @aws-cdk/aws-s3-deletion-protection
   ```

2. Import the required modules in your CDK stack file:
   ```typescript
   import * as cdk from 'aws-cdk-lib';
   import * as s3 from 'aws-cdk-lib/aws-s3';
   import * as s3Encryption from 'aws-cdk-lib/aws-s3-encryption';
   ```

3. Create a new S3 bucket with encryption enabled:
   ```typescript
   const bucket = new s3.Bucket(this, 'MyEncryptedBucket', {
     removalPolicy: cdk.RemovalPolicy.DESTROY,
     encryption: s3Encryption.ServerSideEncryption.S3_MANAGED,
   });
   ```

4. Set the encryption key:
   ```typescript
   bucket.addServerSideEncryptionConfiguration({
     rule: s3Encryption.ServerSideEncryptionByDefault.sseAlgorithm(s3Encryption.ServerSideEncryptionAwsKms.EncryptionAlgorithm.AWS_KMS_MANAGED),
     removalPolicy: cdk.RemovalPolicy.DESTROY,
   });
   ```

5. Set the KMS key for encryption:
   ```typescript
   const kmsKey = new kms.Key(this, 'MyKmsKey', {
     removalPolicy: cdk.RemovalPolicy.DESTROY,
   });
   bucket.addServerSideEncryptionConfiguration({
     rule: s3Encryption.ServerSideEncryptionByDefault.sseAlgorithm(s3Encryption.ServerSideEncryptionAwsKms.EncryptionAlgorithm.AWS_KMS_MANAGED),
     kmsKey: kmsKey,
   });
   ```

6. Set the deletion protection for the bucket:
   ```typescript
   bucket.addRemovalPolicy(cdk.RemovalPolicy.DESTROY);
   ```

7. Export the bucket name for use in other parts of your CDK application:
   ```typescript
   export const bucketName = bucket.bucketName;
   ```

By following these steps, you will have created an S3 bucket using AWS CDK with encryption enabled and a KMS key for encryption. The bucket will also have deletion protection set to destroy, which means it will be deleted when the stack is destroyed. You can use the exported `bucketName` variable to access the bucket name in other parts of your CDK application.