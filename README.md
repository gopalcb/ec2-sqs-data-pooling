<h4>Poll SQS queue messages with boto3:</h4>


```python
from aws_assume_role import *
from sqs_queue_poll import *
```

STS: Assume AWS role and return sqs queue client.


```python
sqs_client = sts_assume_role('sqs')
```

Helper functions details:

Create SQS queue-


```python
def create_sqs_queue(queue_name):
    """
    output syntax
    {
        'QueueUrl': 'https://us-east-1.queue.amazonaws.com/xxxx/sqs-queue', 
        'ResponseMetadata': {
            'RequestId': 'xxxxxxxxx', 
            'HTTPStatusCode': 200, 
            'HTTPHeaders': {
                'x-amzn-requestid': 'xxxxxxxxx', 
                'date': 'date time', 
                'content-type': 'text/xml', 
                'content-length': '334'
            }
        }
    }

    """
    try:
        sqs_client = sts_assume_role('sqs')
        
        response = sqs_client.create_queue(
            QueueName=queue_name,
            Attributes={
                'DelaySeconds': '0',
                'VisibilityTimeout': '60',  # 60 seconds
                'ReceiveMessageWaitTimeSeconds': '20'  # 20 seconds
            }
        )

        if response['ResponseMetadata']['HTTPStatusCode'] == 200:
            return True, response['QueueUrl']
            
        return False, None
        
    except Exception as e:
        print(f'ERROR: {traceback.format_exc()}')
        return False, None
```

Get SQS queue URL if the queue exists-


```python
def get_sqs_queue_url(queue_name):
    """
    output:
    {
        'QueueUrl': 'https://us-east-1.queue.amazonaws.com/xxxx/sqs-queue'
    }
    """
    try:
        sqs_client = sts_assume_role('sqs')
        response = sqs_client.get_queue_url(
            QueueName=queue_name,
        )
        return response['QueueUrl']
        
    except Exception as e:
        print(f'ERROR: {traceback.format_exc()}')
        return ''
```

Send messages to a valid SQS queue-


```python
def send_message_to_sqs_queue(queue_name, messages):
    """
    messages: list(dict)
    messages = [
        {'key1': 'value', ...},
        {'key2': 'value', ...},
        ...
    ]

    output:
    {
        'MD5OfMessageBody': 'xxxxxxx', 
        'MessageId': 'xxxxxxx', 
        'ResponseMetadata': {
            'RequestId': 'xxxxxxx', 
            'HTTPStatusCode': 200, 
            'HTTPHeaders': {
                'x-amzn-requestid': 'xxxxxxx', 
                'date': 'date time', 
                'content-type': 'text/xml', 
                'content-length': '378'
            }
        }
    }
    """
    try:
        sqs_client = sts_assume_role('sqs')
        queue_url = get_sqs_queue_url(queue_name)
        if not queue_url:
            raise Exception('ERROR: Queue not found')
    
        response = sqs_client.send_message(
            QueueUrl=queue_url,
            MessageBody=json.dumps(messages)
        )
        
        if response['ResponseMetadata']['HTTPStatusCode'] == 200:
            data = (response['MD5OfMessageBody'], response['MessageId'])
            return True, data
    
        return False, None

    except Exception as e:
        print(f'ERROR: {traceback.format_exc()}')
        return False, None
```

Long polling a valid SQS queue-


```python
def long_poll_sqs_queue(queue_name):
    """
    output:
    {
        'Messages': [
            {
                'MessageId': 'string',
                'ReceiptHandle': 'string',
                'MD5OfBody': 'string',
                'Body': 'string',
                'Attributes': {
                    'string': 'string'
                },
                'MD5OfMessageAttributes': 'string',
                'MessageAttributes': {
                    'string': {
                        'StringValue': 'string',
                        'BinaryValue': b'bytes',
                        'StringListValues': [
                            'string',
                        ],
                        'BinaryListValues': [
                            b'bytes',
                        ],
                        'DataType': 'string'
                    }
                }
            },
        ]
    }
    """
    try:
        sqs_client = sts_assume_role('sqs')
        queue_url = get_sqs_queue_url(queue_name)
        if not queue_url:
            raise Exception('ERROR: Queue not found')
            
        response = sqs_client.receive_message(
            QueueUrl=queue_url,
            MaxNumberOfMessages=1,
            WaitTimeSeconds=20,
        )

        messages = response.get('Messages', [])
        return messages

    except Exception as e:
        print(f'ERROR: {traceback.format_exc()}')
        return []
```
