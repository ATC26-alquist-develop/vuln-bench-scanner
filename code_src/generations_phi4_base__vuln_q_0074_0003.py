Using AWS Key Management Service (KMS) keys with Amazon S3 buckets in a Cloud Development Kit (CDK) project is a common practice to ensure that your S3 buckets are encrypted at rest. Here's a step-by-step guide on how to do this:

1. **Create a KMS Key:**
   First, you need to create a KMS key that will be used to encrypt your S3 bucket.

   ```typescript
   import * as kms from '@aws-cdk/aws-kms';
   import * as cdk from '@aws-cdk/core';

   class MyStack extends cdk.Stack {
     constructor(scope: cdk.Construct, id: string, props?: cdk.StackProps) {
       super(scope, id, props);

       const key = new kms.Key(this, 'MyKey', {
         description: 'KMS key for encrypting S3 buckets',
         removalPolicy: cdk.RemovalPolicy.DESTROY, // Be cautious with this in production
       });
     }
   }
   ```

2. **Create an S3 Bucket with KMS Encryption:**
   Next, create an S3 bucket and specify the KMS key for encryption.

   ```typescript
   import * as s3 from '@aws-cdk/aws-s3';

   // Inside your stack constructor
   const bucket = new s3.Bucket(this, 'MyEncryptedBucket', {
     encryption: s3.BucketEncryption.s3Managed(key: key),
   });
   ```

3. **Set Bucket Policies (Optional):**
   If you want to restrict access to the bucket, you can set a bucket policy.

   ```typescript
   bucket.addToResourcePolicy(new iam.PolicyStatement({
     actions: ['s3:GetObject', 's3:PutObject'],
     resources: [bucket.bucketArn + '/*'],
     principals: [new iam.AnyPrincipal()],
   }));
   ```

4. **Deploy Your Stack:**
   Finally, deploy your stack to create the resources.

   ```typescript
   const app = new cdk.App();
   new MyStack(app, 'MyStack');
   app.synth();
   ```

5. **Use the CDK CLI to Deploy:**
   Run the following command to deploy your stack:

   ```bash
   cdk deploy
   ```

6. **Accessing the Bucket:**
   Once deployed, you can access the S3 bucket using the AWS Management Console, AWS CLI, or SDKs. Remember that the bucket will be encrypted with the KMS key you created.

7. **Cleanup:**
   After you're done, you can destroy the stack to remove the resources.

   ```bash
   cdk destroy MyStack
   ```

Remember to handle your KMS keys securely and follow best practices for key management. Avoid using the `removalPolicy: cdk.RemovalPolicy.DESTROY` in production environments, as it will delete the key when the stack is destroyed. Instead, use `RemovalPolicy.RETAIN` and manage the key's lifecycle manually.

Also, be aware of the costs associated with using KMS and S3, as they are separate services with their own pricing models.