import boto3
import os

def sts_assume_role(resource_name):
    """
    assume role using aws security token service
    {
        'Credentials': {
            'AccessKeyId': 'xxxx',
            'SecretAccessKey': 'xxxx',
            'SessionToken': 'XXX',
            'Expiration': datetime.datetime(2022, 9, 30, 20, 56, 6, tzinfo=tzutc())
        },
        'AssumedRoleUser': {'AssumedRoleId': 'AROA2V2OH2EKNKNXNBG5Q:TestSession',
        'Arn': 'arn:aws:sts::xxx:assumed-role/s3-readonly-access/TestSession'},
        'ResponseMetadata': {
            'RequestId': 'fa89c2ce-d219-4ecb-af3f-3af0dd84a1dc',
            'HTTPStatusCode': 200,
            'HTTPHeaders': {
                'x-amzn-requestid': 'fa89c2ce-d219-4ecb-af3f-3af0dd84a1dc',
                'content-type': 'text/xml',
                'content-length': '1063',
                'date': 'Fri, 30 Sep 2022 19:56:06 GMT'},
                'RetryAttempts': 0
            }
        }
    """
    profile_name = os.getenv('PROFILE')
    acc_id = os.getenv('ACCOUNT_ID')
    role = os.getenv('ROLE')
    
    session = boto3.Session(profile_name=profile_name)
    sts = session.client('sts')
    response = sts.assume_role(
        RoleArn=f'arn:aws:iam::{acc_id}:role/{role}',
        RoleSessionName=f'{resource_name}-session'
    )
    
    new_session = boto3.Session(
        aws_access_key_id=response['Credentials']['AccessKeyId'],
        aws_secret_access_key=response['Credentials']['SecretAccessKey'],
        aws_session_token=response['Credentials']['SessionToken']
    )
    client = new_session.client(resource_name, region_name='us-east-1')
    
    return client
