import os

# AWS S3 configuration
S3_BUCKET = os.getenv('S3_BUCKET', 'your-s3-bucket')

# DynamoDB table configuration
DYNAMO_TABLE = os.getenv('DYNAMO_TABLE', 'UserFiles')

# SNS topic configuration
SNS_TOPIC_ARN = os.getenv('SNS_TOPIC_ARN', 'arn:aws:sns:region:account-id:topic-name')

# Lambda function name (optional if you want to configure it globally)
LAMBDA_FUNCTION_NAME = os.getenv('LAMBDA_FUNCTION_NAME', 'FileProcessorLambda')
