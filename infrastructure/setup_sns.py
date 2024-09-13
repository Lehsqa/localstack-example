import localstack_client.session as boto3
from botocore.exceptions import ClientError

# Configuration
SNS_TOPIC_NAME = 'FileProcessingTopic'
region = 'us-east-2'  # Set your desired AWS region

# Initialize SNS client
sns = boto3.client('sns', region_name=region)

def create_sns_topic(topic_name):
    try:
        response = sns.create_topic(Name=topic_name)
        sns_topic_arn = response['TopicArn']
        print(f"SNS topic '{topic_name}' created with ARN: {sns_topic_arn}")
        return sns_topic_arn
    except ClientError as e:
        print(f"Error creating SNS topic: {e}")

def subscribe_to_topic(topic_arn, protocol, endpoint):
    try:
        sns.subscribe(
            TopicArn=topic_arn,
            Protocol=protocol,
            Endpoint=endpoint
        )
        print(f"Subscribed {endpoint} to topic {topic_arn}.")
    except ClientError as e:
        print(f"Error subscribing to SNS topic: {e}")

if __name__ == '__main__':
    sns_topic_arn = create_sns_topic(SNS_TOPIC_NAME)

    # Subscribe to the topic (you can change the protocol and endpoint)
    email_endpoint = 'your-email@example.com'
    subscribe_to_topic(sns_topic_arn, 'email', email_endpoint)  # Replace with desired protocol and endpoint
