import json
from lambda_function import process_file
import boto3
from botocore.exceptions import ClientError

# Initialize SNS client
sns = boto3.client('sns')

# Configuration
SNS_TOPIC_ARN = 'arn:aws:sns:us-east-2:000000000000:FileProcessingTopic'  # Replace with your SNS topic ARN

def lambda_handler(event, context):
    """
    AWS Lambda handler function, triggered when a file is uploaded.
    Processes the file and sends an SNS notification.
    """
    # Get the filename and username from the event payload
    filename = event.get('filename')
    username = event.get('username')

    if not filename or not username:
        return {
            'statusCode': 400,
            'body': json.dumps('Invalid input: filename and username are required.')
        }

    print(f"Lambda triggered for file '{filename}' and user '{username}'.")

    # Process the file
    try:
        success = process_file(filename, username)
        if success:
            # If file processing succeeds, send SNS notification
            try:
                sns.publish(
                    TopicArn=SNS_TOPIC_ARN,
                    Message=f"File '{filename}' for user '{username}' has been processed successfully.",
                    Subject='File Processing Complete'
                )
                print(f"SNS notification sent for file '{filename}' and user '{username}'.")
            except ClientError as e:
                print(f"Error sending SNS notification: {e}")
                return {
                    'statusCode': 500,
                    'body': json.dumps('Error sending SNS notification.')
                }

        return {
            'statusCode': 200,
            'body': json.dumps(f"File '{filename}' processed successfully.")
        }
    except Exception as e:
        print(f"Error processing file: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps('Error processing file.')
        }
