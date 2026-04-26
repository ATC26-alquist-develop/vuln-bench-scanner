When using AWS Cloud Development Kit (CDK) to manage your AWS resources, including Amazon S3 buckets and AWS Key Management Service (KMS) keys, you can leverage CDK constructs to manage these resources in a more declarative and type-safe way. Below is an example of how you can use KMS keys with S3 buckets in a CDK project.

### Prerequisites
- Ensure you have the AWS CDK installed and configured in your development environment.
- Have the necessary permissions to create and manage S3 buckets and KMS keys.

### Example CDK Code

```typescript
import * as cdk from 'aws-cdk-lib';
import * as s3 from 'aws-cdk-lib/aws-s3';
import * as kms from 'aws-cdk-lib/aws-kms';

export class S3KMSStack extends cdk.Stack {
  constructor(scope: cdk.App, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    // Create a KMS key
    const kmsKey = new kms.Key(this, 'MyKmsKey', {
      description: 'My KMS Key for S3 buckets',
      enableKeyRotation: true,
    });

    // Create an S3 bucket with a KMS key for encryption
    const bucket = new s3.Bucket(this, 'MyS3Bucket', {
      bucketName: 'my-bucket-name',
      encryption: s3.BucketEncryption.KMS,
      encryptionKey: kmsKey,
    });

    // Optionally, you can also specify the encryption key for a specific object
    const object = bucket.putObject({
      key: 'my-object-key',
      body: 'Hello, world!',
      serverSideEncryption: s3.ObjectServerSideEncryption.KMS,
      serverSideEncryptionKey: kmsKey,
    });
  }
}

// To deploy the stack, run:
// npx cdk deploy S3KMSStack --require-approval never
```

### Explanation

1. **KMS Key Creation**:
   - A KMS key is created using the `kms.Key` construct. You can configure various properties such as `description`, `enableKeyRotation`, and `keyPolicy`.
   - The `keyPolicy` allows you to define the permissions for the KMS key.

2. **S3 Bucket Creation**:
   - An S3 bucket is created using the `s3.Bucket` construct.
   - The `encryption` property is set to `s3.BucketEncryption.KMS`, which specifies that the bucket should be encrypted using the KMS key.
   - Alternatively, you can specify the encryption key for a specific object using the `serverSideEncryption` and `serverSideEncryptionKey` properties.

### Additional Considerations

- **Key Policy**: Ensure that the KMS key policy allows the necessary permissions for the S3 bucket and any other AWS services that might need to interact with the KMS key.
- **Rotation**: The `enableKeyRotation` property is set to `true` to enable automatic rotation of the KMS key, which is a best practice for security.
- **Permissions**: Ensure that the IAM roles and policies associated with your S3 bucket and KMS key are correctly configured to allow the necessary access.

### Deploying the Stack

To deploy the stack, you can use the following command:

```bash
npx cdk deploy S3KMSStack --require-approval never
```

This command will deploy the stack and automatically create the KMS key and S3 bucket with the specified encryption settings.

### Conclusion

Using CDK to manage KMS keys and S3 buckets allows for a more declarative and type-safe approach to AWS resource management. By leveraging the CDK constructs, you can easily define and manage your resources, ensuring that your infrastructure is secure and scalable.