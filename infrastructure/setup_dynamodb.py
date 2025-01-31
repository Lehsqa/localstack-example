import localstack_client.session as boto3
from botocore.exceptions import ClientError

# Configuration
DYNAMO_TABLE = 'UserFiles'  # Table to store user file metadata
region = 'us-east-2'  # Set your desired AWS region

# Initialize DynamoDB client
dynamodb = boto3.client('dynamodb', region_name=region)


def create_dynamodb_table(table_name):
    try:
        response = dynamodb.create_table(
            TableName=table_name,
            KeySchema=[
                {
                    'AttributeName': 'Username',
                    'KeyType': 'HASH'  # Partition key
                },
                {
                    'AttributeName': 'Filename',
                    'KeyType': 'RANGE'  # Sort key
                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'Username',
                    'AttributeType': 'S'  # String
                },
                {
                    'AttributeName': 'Filename',
                    'AttributeType': 'S'  # String
                }
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5
            }
        )
        print(f"DynamoDB table '{table_name}' created successfully.")
    except ClientError as e:
        print(f"Error creating DynamoDB table: {e}")


if __name__ == '__main__':
    create_dynamodb_table(DYNAMO_TABLE)
