import boto3
from pprint import pprint
# Replace with your Amazon Connect Instance ID
INSTANCE_ID = '394168b7-6fe9-4b77-9fcf-2bddc3a1b03c'

client = boto3.client('connect', region_name='us-east-1')  # region_name can also be specified

users = []
next_token = None

while True:
    if next_token:
        response = client.list_users(
            InstanceId=INSTANCE_ID,
            MaxResults=100,
            NextToken=next_token
        )
    else:
        response = client.list_users(
            InstanceId=INSTANCE_ID,
            MaxResults=100
        )
    users.extend(response.get('UserSummaryList', []))
    next_token = response.get('NextToken')
    if not next_token:
        break

for user in users:
    pprint(f"User ID: {user['Id']}, Username: {user['Username']}, ARN: {user['Arn']}")
