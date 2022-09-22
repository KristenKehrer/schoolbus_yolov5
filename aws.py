import os

os.environ['AWS_SHARED_CREDENTIALS_FILE'] = '.aws_credentials'

import boto3


def test_aws_access() -> bool:
    """
    We only try to use aws on detection, so I call this on startup of detect_bus.py to make sure credentials
    are working and everything.  I got sick of having the AWS code fail hours after starting up detect_bus.py...
    I googled how to check if boto3 is authenticated, and found this:
    https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sts.html#STS.Client.get_caller_identity
    """
    try:
        resp = boto3.client('sts').get_caller_identity()
        print(f'AWS credentials working.')
        return True
    except Exception as e:
        print(f'Failed to validate AWS authentication: {e}')
        return False


def send_sms(msg):
    boto3.client('sns').publish(
        TopicArn='arn:aws:sns:us-east-1:916437080264:detect_bus',
        Message=msg,
        Subject='bus detector',
        MessageStructure='string')


def save_file(file_path, content_type='image/jpeg'):
    """Save a file to our s3 bucket (file storage in AWS) because we wanted to include an image in the text"""
    client = boto3.client('s3')
    client.upload_file(file_path, 'bus-detector', file_path,
                       ExtraArgs={'ACL': 'public-read', 'ContentType': content_type})
    return f'https://bus-detector.s3.amazonaws.com/{file_path}'
