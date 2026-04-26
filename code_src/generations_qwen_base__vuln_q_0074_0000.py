To create an S3 bucket using AWS Cloud Development Kit (AWS CDK) and encrypt its contents, you can follow these steps. AWS CDK is a software development framework for AWS that allows you to define your AWS infrastructure in a programming language of your choice, and then deploy it to AWS.

### Prerequisites
- Install AWS CDK CLI and the AWS CDK for your preferred programming language (e.g., TypeScript, Python, Java, etc.).
- Ensure you have an AWS account and the necessary permissions to create S3 buckets and configure encryption.

### Step 1: Install AWS CDK CLI and the AWS CDK for Your Preferred Language

If you haven't already, you can install the AWS CDK CLI globally on your machine:

```bash
npm install -g aws-cdk
```

For a specific language, you can install the AWS CDK CLI for that language:

```bash
npm install -g aws-cdk@latest
```

### Step 2: Create a New CDK Project

You can create a new CDK project using the AWS CDK CLI:

```bash
cdk init app --language=typescript
```

This command will create a new CDK project with a TypeScript template.

### Step 3: Define the S3 Bucket with Encryption

In your CDK app, you can define an S3 bucket and configure encryption. Here's an example using TypeScript:

```typescript
import * as cdk from 'aws-cdk-lib';
import * as s3 from 'aws-cdk-lib/aws-s3';
import * as s3object from 'aws-cdk-lib/aws-s3-object-lock';

export class S3BucketStack extends cdk.Stack {
  constructor(scope: cdk.App, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    // Define the S3 bucket
    const bucket = new s3.Bucket(this, 'MyEncryptedBucket', {
      encryption: s3.BucketEncryption.KMS_MANAGED,
      removalPolicy: cdk.RemovalPolicy.DESTROY, // Change to cdk.RemovalPolicy.RETAIN if you want to keep the bucket
    });

    // Optionally, you can enable Object Lock on the bucket
    const objectLockEnabled = new s3object.ObjectLockEnabled(this, 'ObjectLockEnabled', {
      bucket: bucket,
      lockEnabled: true,
    });

    // Optionally, you can set default encryption for the bucket
    bucket.defaultEncryptionConfiguration({
      serverSideEncryptionConfiguration: [
        {
          bucketKeyEnabled: true,
          serverSideEncryptionByDefault: {
            sseAlgorithm: s3.BucketEncryption.AES256,
          },
        },
      ],
    });
  }
}

// To deploy the stack, run:
// cdk deploy
```

### Explanation

- **Encryption**: The `encryption` property is set to `s3.BucketEncryption.KMS_MANAGED`, which means the bucket will use AWS Key Management Service (KMS) to manage encryption keys. You can also use `s3.BucketEncryption.SSE_S3` for server-side encryption using Amazon S3-managed keys.
  
- **Object Lock**: The `objectLockEnabled` property enables Object Lock on the bucket. You can configure Object Lock to enforce retention policies and set default retention periods.

- **Default Encryption**: The `defaultEncryptionConfiguration` method sets the default encryption configuration for the bucket. In this example, it enables server-side encryption using AES256.

### Step 4: Deploy the Stack

After defining your stack, you can deploy it to AWS:

```bash
cdk deploy
```

This will create the S3 bucket with the specified encryption settings.

### Step 5: (Optional) Configure Encryption for Existing Buckets

If you already have an S3 bucket and want to encrypt its contents, you