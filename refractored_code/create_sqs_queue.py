from botocore.exceptions import ClientError, ParamValidationError

def create_sqs_queue(sqs_client, sqs_queue_name):
    try:
        data = sqs_client.create_queue( # Creates a new standard queue
            QueueName=sqs_queue_name, # Requests name (as string) of new queue
            Attributes={
                'RecieveMessageWaitTimeSeconds': '20',
                'VisibilityTimeout': '60'
            }
        )
        return data['QueueUrl']
    
    except ParamValidationError as e:
        print("Parameter validation error: %s" % e)
    except ClientError as e:
        print("Client error: %s" % e)