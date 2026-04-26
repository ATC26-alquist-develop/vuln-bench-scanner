Certainly! To set up an Amazon S3 bucket using AWS Cloud Development Kit (CDK) to store customer financial records, you'll need to follow these steps:

1. Install the AWS CDK CLI if you haven't already. You can install it using npm:

```bash
npm install -g aws-cdk
```

2. Initialize a new CDK project in your preferred language. For this example, we'll use TypeScript:

```bash
cdk init app --language=typescript
```

3. Install the necessary CDK libraries for S3:

```bash
npm install @aws-cdk/aws-s3
```

4. Open the `lib/your-app-stack.ts` file (replace `your-app-stack` with the name of your stack) and add the following code to define an S3 bucket:

```typescript
import * as cdk from '@aws-cdk/core';
import * as s3 from '@aws-cdk/aws-s3';

export class YourAppStack extends cdk.Stack {
  constructor(scope: cdk.Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    const financialRecordsBucket = new s3.Bucket(this, 'FinancialRecordsBucket', {
      removalPolicy: cdk.RemovalPolicy.DESTROY, // Be careful with this in production
      blockPublicAccess: s3.BlockPublicAccess.BLOCK_ALL,
      encryption: s3.BucketEncryption.S3_MANAGED,
      // Add any additional bucket configurations here
    });

    // Output the bucket name
    new cdk.CfnOutput(this, 'BucketName', { value: financialRecordsBucket.bucketName });
  }
}
```

5. Deploy the stack to your AWS account:

```bash
cdk deploy
```

This code snippet creates an S3 bucket with the following configurations:

- `removalPolicy: cdk.RemovalPolicy.DESTROY` - This will delete the bucket when the stack is destroyed. Be cautious with this setting in production, as it will permanently delete the bucket and its contents.
- `blockPublicAccess: s3.BlockPublicAccess.BLOCK_ALL` - This ensures that the bucket is not publicly accessible.
- `encryption: s3.BucketEncryption.S3_MANAGED` - This enables S3-managed encryption for the bucket.

6. After deploying the stack, you will receive an output with the bucket name, which you can use to access the bucket in your AWS Management Console or through the AWS CLI.

Remember to replace `YourAppStack` with the actual name of your stack and adjust the bucket configurations as needed for your specific use case. Also, be sure to handle the removal policy appropriately for production environments to avoid accidental data loss.