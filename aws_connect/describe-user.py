import boto3
from pprint import pprint

INSTANCE_ID = '394168b7-6fe9-4b77-9fcf-2bddc3a1b03c'

client = boto3.client('connect', region_name='us-east-1')

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

# Find user with username "kb"
kb_user_id = None
for user in users:
    if user['Username'] == 'kb':
        kb_user_id = user['Id']
        break

if kb_user_id:
    print(f"Found kb user with ID: {kb_user_id}")
    # Call describe_user API to get detailed info
    kb_user_details = client.describe_user(
        InstanceId=INSTANCE_ID,
        UserId=kb_user_id
    )
    pprint(kb_user_details['User'])
else:
    print("User with username 'kb' not found.")
