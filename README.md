# LocalStack AWS Services Example

This project demonstrates how to set up and use various AWS services locally using LocalStack. It includes a Flask web application for file uploads, along with infrastructure setup scripts for S3, DynamoDB, SNS, and Lambda.

## Project Structure

```
localstack-example/
├── app/
│   ├── __init__.py
│   ├── app.py
│   ├── config.py
│   └── templates/
│       └── index.html
├── ec2-flask/
│   ├── run.sh
│   └── user_script.sh
├── infrastructure/
│   ├── setup_dynamodb.py
│   ├── setup_lambda.py
│   ├── setup_s3.py
│   └── setup_sns.py
├── lambda/
│   ├── lambda_function.py
│   ├── lambda_handler.py
│   └── requirements.txt
└── commands
```

## Setup

1. Start LocalStack:
   ```
   docker run --rm -it -p 127.0.0.1:4566:4566 -p 127.0.0.1:4510-4559:4510-4559 -v /var/run/docker.sock:/var/run/docker.sock localstack/localstack
   ```

2. Set up AWS services:
   ```
   python setup_s3.py
   python setup_sns.py
   python setup_dynamodb.py
   python setup_lambda.py
   ```

3. Run the Flask application:
   ```
   python app.py
   ```

## Components

### Flask Application (app/app.py)
- Handles file uploads
- Interacts with S3, DynamoDB, and Lambda
- Provides a simple web interface for file uploads

### Infrastructure Setup
- `setup_s3.py`: Creates an S3 bucket
- `setup_sns.py`: Sets up an SNS topic
- `setup_dynamodb.py`: Creates a DynamoDB table
- `setup_lambda.py`: Deploys a Lambda function

### Lambda Function (lambda/)
- Processes uploaded files
- Updates DynamoDB with file status
- Sends SNS notifications

### EC2 Flask Setup (ec2-flask/)
- Scripts for setting up a Flask application on EC2 (for demonstration purposes)

## Usage

1. Access the web interface at `http://localhost:80`
2. Upload a file using the provided form
3. The file will be processed by the Lambda function
4. Check the file status using the `/status/<username>/<filename>` endpoint

## Configuration

Adjust the configuration in `app/config.py` to match your LocalStack setup:

- S3_BUCKET
- DYNAMO_TABLE
- SNS_TOPIC_ARN
- LAMBDA_FUNCTION_NAME

## Notes

- This project is designed for local development and testing with LocalStack
- Ensure all necessary Python dependencies are installed
- Modify IAM roles and permissions as needed for your specific use case (example in commands file for lambda)
