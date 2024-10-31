# Load the AWS SDK for Python
import boto3
import time

# Load the exceptions for error handling
from botocore.exceptions import ClientError, ParamValidationError

# Create AWS service client and set region
sqs = boto3.client('sqs', region_name='us-east-1')

# Create an SQS queue
def create_sqs_queue(sqs_queue_name):
    try:
        data = sqs.create_queue(
            QueueName = sqs_queue_name,
            Attributes = {
                'ReceiveMessageWaitTimeSeconds': '20',
                'VisibilityTimeout': '60'
            }
        )
        return data['QueueUrl']
    # An error occurred
    except ParamValidationError as e:
        print("Parameter validation error: %s" % e)
    except ClientError as e:
        print("Client error: %s" % e)


# # Function to send 50 SQS messsages ***1 at a time is slow***
# def create_messages(queue_url):
#     # Create 50 messages
#     TempMessages = []
#     for a in range(50):
#         tempStr = 'This is the content for message ' + str(a)
#         TempMessages.append(tempStr) # Make a Message-List with 50 messages

#     # Send those messages to SQS queue_url
#     for message in TempMessages:
#         try:
#             data = sqs.send_message(
#                 QueueUrl = queue_url,
#                 MessageBody = message
#             )
#             print(data['MessageId'])
#         # Exception Handling
#         except ParamValidationError as e:
#             print("Parameter validation error: %s" % e)
#         except ClientError as e:
#             print("Client error: %s" % e)

## Increase Throughput with "sendMessageBatch" function
    # Send 10 messages at a time
    # Change our array to 2D to accomodate 5 batches x 10 messages

def create_messages(queue_url):
    # Create 50 messages in batches of 10
    TempMessages = []
    for a in range(5):
        TempEntries = []
        for b in range(10):
            tempStr1 = 'This is the content for message ' + str((a*10 + b))
            tempStr2 = 'Message' + str((a*10 + b))
            tempEntry = {
                'MessageBody': tempStr1,
                'Id': tempStr2
            }
            TempEntries.append(tempEntry)
        TempMessages.append(TempEntries)
    
    # Deliver messages to SQS queue_url
    for batch in TempMessages:
        try:
            data = sqs.send_message_batch(
                QueueUrl = queue_url,
                Entries = batch
            )
            print(data['Successful']) # Special Dictionary as-specified in the AWS API Documentation
        # Error Handling
        except ParamValidationError as e:
            print("Parameter validation error: %s" % e)
        except ClientError as e:
            print("Client error: %s" % e)

## Create Receive Messages Function in order to Process them
def receive_messages(queue_url):
    print('Reading messages')
    while True: # Loops through Continuously // If no ==> time.sleep(60)
        try:
            data = sqs.receive_message( # Dictionary defined in the AWS API Documentation
                QueueUrl = queue_url,
                MaxNumberOfMessages = 10,
                VisibilityTimeout = 60,
                WaitTimeSeconds = 20
            )
        # An error occurred
        except ParamValidationError as e:
            print("Parameter validation error: %s" % e)
        except ClientError as e:
            print("Client error: %s" % e)
        else:
            # Check if empty receive
            try:
                data['Messages']
            except KeyError:
                data = None
            if data is None:
                print('Queue empty waiting 60s')
                # Wait for 60 seconds
                time.sleep(60)
            else:
                for message in data['Messages']:
                    print(message)
                    sqs.delete_message(
                        QueueUrl=queue_url,
                        ReceiptHandle=message['ReceiptHandle']
                    )
                    print('Deleted message')
                    # Wait for 1 second
                    # time.sleep(1)
            # Do not forget to add this call to the main program
            # Gotta process them and delete from the queue now
 
# Main program
def main():
    sqs_queue_url = create_sqs_queue('backspace-lab')
    print('Successfully created SQS queue URL '+ sqs_queue_url )
    create_messages(sqs_queue_url)
    print("Successfully sent 50 messages to the SQS queue")
    receive_messages(sqs_queue_url)

if __name__ == '__main__':
    main()
    
