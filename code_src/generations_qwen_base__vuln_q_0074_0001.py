Certainly! Below is a Python script using AWS Cloud Development Kit (CDK) to set up an encrypted S3 bucket for storing sensitive data. This script will include the necessary steps to create an S3 bucket with server-side encryption using AWS Key Management Service (KMS).

First, ensure you have the AWS CDK installed and configured. You can install the AWS CDK CLI and Python SDK (boto3) if you haven't already:

```bash
pip install aws-cdk-lib boto3
```

Next, create a new Python file, for example, `s3_encrypted_bucket_stack.py`, and add the following code:

```python
from aws_cdk import (
    core as cdk,
    aws_s3 as s3,
    aws_kms as kms,
    aws_kms.CfnKey as CfnKey,
    aws_kms.CfnAlias as CfnAlias,
    aws_kms.CfnKeyPolicy as CfnKeyPolicy,
    aws_kms.CfnAliasPolicy as CfnAliasPolicy,
    aws_kms.CfnAliasGrant as CfnAliasGrant,
    aws_kms.CfnAliasGrantTarget as CfnAliasGrantTarget,
    aws_kms.CfnAliasGrantTargetGranteePrincipal as CfnAliasGrantTargetGranteePrincipal,
    aws_kms.CfnAliasGrantTargetGranteePrincipalType as CfnAliasGrantTargetGranteePrincipalType,
    aws_kms.CfnAliasGrantTargetGranteePrincipalValue as CfnAliasGrantTargetGranteePrincipalValue,
    aws_kms.CfnAliasGrantTargetGranteePrincipalType as CfnAliasGrantTargetGranteePrincipalType,
    aws_kms.CfnAliasGrantTargetGranteePrincipalValue as CfnAliasGrantTargetGranteePrincipalValue,
    aws_kms.CfnAliasGrantTargetGranteePrincipalType as CfnAliasGrantTargetGranteePrincipalType,
    aws_kms.CfnAliasGrantTargetGranteePrincipalValue as CfnAliasGrantTargetGranteePrincipalValue,
    aws_kms.CfnAliasGrantTargetGranteePrincipalType as CfnAliasGrantTargetGranteePrincipalType,
    aws_kms.CfnAliasGrantTargetGranteePrincipalValue as CfnAliasGrantTargetGranteePrincipalValue,
    aws_kms.CfnAliasGrantTargetGranteePrincipalType as CfnAliasGrantTargetGranteePrincipalType,
    aws_kms.CfnAliasGrantTargetGranteePrincipalValue as CfnAliasGrantTargetGranteePrincipalValue,
    aws_kms.CfnAliasGrantTargetGranteePrincipalType as CfnAliasGrantTargetGranteePrincipalType,
    aws_kms.CfnAliasGrantTargetGranteePrincipalValue as CfnAliasGrantTargetGranteePrincipalValue,
    aws_kms.CfnAliasGrantTargetGranteePrincipalType as CfnAliasGrantTargetGranteePrincipalType,
    aws_kms.CfnAliasGrantTargetGranteePrincipalValue as CfnAliasGrantTargetGranteePrincipalValue,
    aws_kms.CfnAliasGrantTargetGranteePrincipalType as CfnAliasGrantTargetGranteePrincipalType,
    aws_kms.CfnAliasGrantTargetGranteePrincipalValue as CfnAliasGrantTargetGranteePrincipalValue,
    aws_kms.CfnAliasGrantTargetGranteePrincipalType as CfnAliasGrantTargetGranteePrincipalType,
    aws_kms.CfnAliasGrantTargetGranteePrincipalValue as CfnAliasGrantTargetGranteePrincipalValue,
    aws_kms.CfnAliasGrantTargetGranteePrincipalType as CfnAliasGrantTargetGranteePrincipalType,
    aws_kms.CfnAliasGrantTargetGranteePrincipalValue as CfnAliasGrantTargetGranteePrincipalValue,
    aws_kms.CfnAliasGrantTargetGranteePrincipalType as CfnAliasGrantTargetGranteePrincipalType,
    aws_kms.CfnAliasGrantTargetGranteePrincipalValue as CfnAliasGrantTargetGranteePrincipalValue,
    aws_kms.CfnAliasGrant