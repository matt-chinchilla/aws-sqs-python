# Initializes SQS client
import boto3

def initialize_sqs_client(region = 'us-east-1'):
    return boto3.client('sqs', region_name = region)

# Take in region parameter, Then returns client for sqs