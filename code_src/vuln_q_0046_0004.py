```python
import boto3
import os
import logging
from botocore.exceptions import ClientError
from typing import Optional

def change_encryption_key(
    kms_client: boto3.client,
    source_key_id: str,
    destination_key_id: str,
    source_arn: str,
    destination_arn: str,
    kms_key_arn: str,
    kms_key_alias: str,
    kms_key_alias_arn: str,
    kms_key_alias_arn_arn: str,
    kms_key_alias_arn_arn_arn: str,
    kms_key_alias_arn_arn_arn_arn: str,
    kms_key_alias_arn_arn_arn_arn_arn: str,
    kms_key_alias_arn_arn_arn_arn_arn_arn: str,
    kms_key_alias_arn_arn_arn_arn_arn_arn_arn: str,
    kms_key_alias_arn_arn_arn_arn_arn_arn_arn_arn: str,
    kms_key_alias_arn_arn_arn_arn_arn_arn_arn_arn_arn: str,
    kms_key_alias_arn_arn_arn_arn_arn_arn_arn_arn_arn_arn: str,
    kms_key_alias_arn_arn_arn_arn_arn_arn_arn_arn_arn_arn_arn: str,
    kms_key_alias_arn_arn_arn_arn_arn_arn_arn_arn_arn_arn_arn_arn: str,
    kms_key_alias_arn_arn_arn_arn_arn_arn_arn_arn_arn_arn_arn_arn_arn: str,
    kms_key_alias_arn_arn_arn_arn_arn_arn_arn_arn_arn_arn_arn_arn_arn_arn: str,
    kms_key_alias_arn_arn_arn_arn_arn_arn_arn_arn_arn_arn_arn_arn_arn_arn_arn: str,
    kms_key_alias_arn_arn_arn_arn_arn_arn_arn_arn_arn_arn_arn_arn_arn_arn_arn_arn: str,
    kms_key_alias_arn_arn_arn_arn_arn_arn_arn_arn_arn_arn_arn_arn_arn_arn_arn_arn_arn: str,
    kms_key_alias_arn_arn_arn_arn_arn_arn_arn_arn_arn_arn_arn_arn_arn_arn_arn_arn_arn: str,
    kms_key_alias_arn_arn_arn_arn_arn_arn_arn_arn_arn_arn_arn_arn_arn_arn_arn_arn_arn: str,
    kms_key_alias_arn_arn_arn_arn_arn_arn_arn_arn_arn_arn_arn_arn_arn_arn_arn_arn_arn: str,
    kms_key_alias_arn_arn_arn_arn_arn_arn_arn_arn_arn_arn_arn_arn_arn_arn_arn_arn_arn: str,
    kms_key_alias_arn_arn_arn_arn_arn_arn_arn_arn_arn_arn_arn_arn_arn_arn_arn_arn_arn: str,
    kms_key_alias_arn_arn_arn_arn_arn_arn_arn_arn_arn_arn_arn_arn_arn_arn_arn_arn_arn: str,
    kms_key_alias_arn_arn_arn_arn_arn_arn_arn_arn_arn_arn_arn_arn_arn_arn_arn_arn_arn: str,
    kms_key_alias