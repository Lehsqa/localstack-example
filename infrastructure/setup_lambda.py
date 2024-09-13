import localstack_client.session as boto3
import zipfile
import os
from botocore.exceptions import ClientError

# Configuration
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LAMBDA_FUNCTION_NAME = 'FileProcessorLambda'
ROLE_ARN = 'arn:aws:iam::000000000000:role/Lambda'  # Replace with your IAM role ARN
ZIP_FILE = 'lambda_function.zip'  # Name of the zipped Lambda function
LAMBDA_HANDLER = 'lambda_handler.lambda_handler'  # File.function_name for Lambda handler
RUNTIME = 'python3.11'
region = 'us-east-2'

# Initialize Lambda client
lambda_client = boto3.client('lambda', region_name=region)

def create_lambda_package():
    # Zip the Lambda function code
    with zipfile.ZipFile(ZIP_FILE, 'w') as zipf:
        zipf.write(f'{ROOT_DIR}/lambda/lambda_function.py', 'lambda_function.py')
        zipf.write(f'{ROOT_DIR}/lambda/lambda_handler.py', 'lambda_handler.py')
    print(f"Created Lambda package: {ZIP_FILE}")

def deploy_lambda_function(function_name, zip_file, handler, runtime, role_arn):
    try:
        with open(zip_file, 'rb') as f:
            zipped_code = f.read()

        response = lambda_client.create_function(
            FunctionName=function_name,
            Runtime=runtime,
            Role=role_arn,
            Handler=handler,
            Code=dict(ZipFile=zipped_code),
            Timeout=300,  # Set timeout in seconds (5 minutes)
            MemorySize=128  # Set memory size in MB
        )
        print(f"Lambda function '{function_name}' created successfully.")
    except ClientError as e:
        print(f"Error creating Lambda function: {e}")

if __name__ == '__main__':
    create_lambda_package()
    deploy_lambda_function(LAMBDA_FUNCTION_NAME, ZIP_FILE, LAMBDA_HANDLER, RUNTIME, ROLE_ARN)
