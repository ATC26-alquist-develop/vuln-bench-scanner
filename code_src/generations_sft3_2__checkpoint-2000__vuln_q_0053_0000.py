import boto3
from boto3.dynamodb.conditions import Attr
from botocore.exceptions import ClientError
import logging
from typing import Optional

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class UserAuth:
    def __init__(self):
        self.dynamodb = boto3.resource('dynamodb')
        self.table_name = 'UserAuthTable'  # Use your actual table name
        
    def verify_user(self, username: str, password: str) -> bool:
        """
        Verify user credentials using Cognito
        """
        try:
            # Verify user with Cognito
            cognito = boto3.client('cognito-idp')
            response = cognito.admin_get_user(
                UserPoolId=os.environ.get('COGNITO_POOL_ID'),
                Username=username
            )
            
            # Verify password using Cognito's verify_password method
            return cognito.verify_password(
                password=password,
                username=username,
                user_pool_id=os.environ.get('COGNITO_POOL_ID')
            )
            
        except ClientError as e:
            logger.error(f"Cognito error: {str(e)}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            return False

    def store_user(self, username: str, password: str) -> bool:
        """
        Store user in DynamoDB
        """
        try:
            # Use AWS Secrets Manager for storing passwords
            secrets_client = boto3.client('secretsmanager')
            secret_name = f'/your-secret-name/{username}'
            secret = secrets_client.get_secret_value(SecretId=secret_name)
            
            # Verify the secret exists
            if 'SecretString' in secret:
                stored_password = secret['SecretString']
            else:
                logger.error("Secret not found")
                return False
                
            # Verify password
            if self.verify_user(username, stored_password):
                # Store user in DynamoDB
                table = self.dynamodb.Table(self.table_name)
                table.put_item(
                    Item={
                        'username': username,
                        'password_hash': stored_password
                    }
                )
                return True
            else:
                return False
                
        except ClientError as e:
            logger.error(f"DynamoDB error: {str(e)}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            return False