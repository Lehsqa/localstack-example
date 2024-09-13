import localstack_client.session as boto3
from botocore.exceptions import ClientError

# Configuration
S3_BUCKET = 'test-s3-bucket-name'  # Replace with your S3 bucket name
region = 'us-east-2'  # Set your desired AWS region

# Initialize S3 client
s3 = boto3.client('s3', region_name=region)

def create_s3_bucket(bucket_name):
    try:
        s3.create_bucket(
            Bucket=bucket_name,
            CreateBucketConfiguration={'LocationConstraint': region}
        )
        print(f"Bucket '{bucket_name}' created successfully.")
    except ClientError as e:
        print(f"Error creating bucket: {e}")

if __name__ == '__main__':
    create_s3_bucket(S3_BUCKET)
