from flask import Flask, request, jsonify, render_template, redirect, url_for
import localstack_client.session as boto3
import os
import json
from botocore.exceptions import NoCredentialsError, ClientError
from config import S3_BUCKET, DYNAMO_TABLE, SNS_TOPIC_ARN

app = Flask(__name__)

# Initialize AWS services
region = 'us-east-2'

s3 = boto3.client('s3', region_name=region)
dynamodb = boto3.resource('dynamodb', region_name=region)
lambda_client = boto3.client('lambda', region_name=region)

table = dynamodb.Table(DYNAMO_TABLE)

@app.route('/')
def index():
    # Render the HTML file upload form (index.html) located in the templates/ folder
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    # Get the username and file from the request
    username = request.form['username']
    file = request.files['file']

    if not username or not file:
        return jsonify({'error': 'Username and file are required'}), 400

    # Save file to S3
    try:
        file_name = file.filename
        s3.upload_fileobj(file, 'test-s3-bucket-name', file_name)
        print(f"File {file_name} uploaded to S3 bucket {S3_BUCKET}.")
    except NoCredentialsError:
        return jsonify({'error': 'S3 credentials not found.'}), 500
    except ClientError as e:
        return jsonify({'error': str(e)}), 500

    # Save metadata to DynamoDB
    try:
        table.put_item(
            Item={
                'Username': username,
                'Filename': file_name,
                'Status': 'Uploaded'
            }
        )
        print(f"File metadata stored in DynamoDB for user {username}.")
    except ClientError as e:
        return jsonify({'error': str(e)}), 500

    # Trigger the Lambda function for file processing
    try:
        lambda_response = lambda_client.invoke(
            FunctionName='FileProcessorLambda',
            InvocationType='Event',  # Asynchronous invocation
            Payload=json.dumps({'filename': file_name, 'username': username})
        )
        print(f"Lambda function invoked for file {file_name}.")
    except ClientError as e:
        return jsonify({'error': str(e)}), 500

    return jsonify({'message': 'File uploaded and processing started.'}), 200

@app.route('/status/<username>/<filename>', methods=['GET'])
def check_status(username, filename):
    # Fetch file status from DynamoDB
    try:
        response = table.get_item(
            Key={
                'Username': username,
                'Filename': filename
            }
        )
        item = response.get('Item')
        if not item:
            return jsonify({'error': 'File not found.'}), 404
        return jsonify({'status': item['Status']}), 200
    except ClientError as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
